from xml.etree import ElementTree
import hashlib
import re


from . import templates


LINK_ELTS = {
    'SUCCESS': (
        ('ordinal', '0'),
        ('color', 'BLUE'),
        ('completeBuild', 'true'),
    ),
    'UNSTABLE': (
        ('ordinal', '1'),
        ('color', 'YELLOW'),
        ('completeBuild', 'true'),
    ),
    'FAILURE':  (
        ('ordinal', '2'),
        ('color', 'RED'),
        ('completeBuild', 'true'),
    ),
}


def extract_pipeline_conf(conf):
    '''
    Remove and parse the pipeline bits in XML job definition *conf*.
    '''
    tree = ElementTree.fromstring(conf)
    rbt_elt = tree.find('.//jenkins.triggers.ReverseBuildTrigger')
    if rbt_elt is not None:
        upstream_projects = rbt_elt.findtext('./upstreamProjects')
        upstream_projects = [x for x in upstream_projects.split(',')
                             if x.strip()]
        upstream_link_type = rbt_elt.findtext('./threshold/name')
        pipe_bits = (upstream_projects, upstream_link_type)
        parent_map = {c: p for p in tree.iter() for c in p}
        parent_map[rbt_elt].remove(rbt_elt)
    else:
        pipe_bits = None
    pruned_conf = _format_xml_tree(tree)
    return pipe_bits, pruned_conf


def _format_xml_tree(tree):
    return ElementTree.tostring(tree, encoding='UTF-8', method='xml')


def merge_pipeline_conf(conf, parents, link_type):
    '''
    Merge back pipeline informations in job configuration *conf*.

    *parents* is a list of parent jobs names, and *link_type* the relationship
    to them (one of "SUCCESS", "UNSTABLE" or "FAILURE").
    '''
    tree = ElementTree.fromstring(conf)
    trigger = _create_elt('jenkins.triggers.ReverseBuildTrigger')
    trigger.append(_create_elt('spec'))
    upstream_projects = _create_elt('upstreamProjects', ', '.join(parents))
    trigger.append(upstream_projects)
    threshold = _create_elt('threshold')
    threshold.append(_create_elt('name', link_type))
    for elt_name, elt_text in LINK_ELTS[link_type]:
        elt = _create_elt(elt_name, elt_text)
        threshold.append(elt)
    trigger.append(threshold)
    triggers = tree.find('.//triggers')
    triggers.append(trigger)
    return _format_xml_tree(tree)


def _create_elt(tag, text=None):
    elt = ElementTree.Element(tag)
    elt.text = text
    return elt


def render_job(templates_dir, template, context, pipe_info, insert_hash=False,
               context_overrides={}):
    '''
    Render a job XML from job definition.

    If *insert_hash* is true, also include a hash of the configuration as text
    in the job description.

    :param templates_dir: location of the jobs templates
    :param template: the path to the job template, relative to *templates_dir*
    :param context: a dict containing the variables passed to the tamplate
    :param pipe_info: a ``(parents, link_type)`` tuple
    :param insert_hash:
        a boolean indicating if a hash of the job config should be inserted in
        the job description
    :param context_overrides:
        a mapping that will be deep merged in the final context
    '''
    rendered = templates.render(templates_dir, template, context,
                                context_overrides=context_overrides)
    rendered = rendered.strip()
    rendered = rendered.encode('utf8')
    if pipe_info is not None:
        parents, link_type = pipe_info
        rendered = merge_pipeline_conf(rendered, parents, link_type)
    if insert_hash:
        rendered = append_hash_in_description(rendered)
    return rendered


def get_conf_hash(conf):
    '''
    Get a hash uniquely representing the XML job configuration *conf*.
    '''
    hobj = hashlib.sha1()
    tree = ElementTree.fromstring(conf)
    for element in tree.iter():
        hobj.update(element.tag.encode('utf8'))
        if element.text is not None:
            hobj.update(element.text.encode('utf8'))
        for key in sorted(element.attrib):
            value = element.attrib[key]
            hobj.update(key.encode('utf8'))
            hobj.update(value.encode('utf8'))
    return hobj.hexdigest()


def append_hash_in_description(conf):
    '''
    Append the *conf* hash at the end of its description.
    '''
    conf_hash = get_conf_hash(conf)
    tree = ElementTree.fromstring(conf)
    description_elt = tree.find('.//description')
    text = description_elt.text if description_elt.text is not None else ''
    text += '\r\n\r\n-*- jenskipper-hash: %s -*-' % conf_hash
    description_elt.text = text
    return _format_xml_tree(tree)


def extract_hash_from_description(conf):
    '''
    Extract jenskiper hash tag from job *conf*'s description.

    Return a ``(hash, pruned_conf)`` tuple, with *hash* the job's hash and
    *pruned_conf* the configuration XML the hash tag removed from its
    description.
    '''
    tree = ElementTree.fromstring(conf)
    description_elt = tree.find('.//description')
    if description_elt is None:
        return None, conf
    text = description_elt.text
    if text is not None:
        conf_hash, text = extract_hash_from_text(text)
        description_elt.text = text
        conf = _format_xml_tree(tree)
    else:
        conf_hash = None
    return conf_hash, conf


def extract_hash_from_text(text):
    match = re.search('(\r?\n){0,2}-\*- jenskipper-hash: ([0-9a-f]+) -\*-',
                      text, re.MULTILINE)
    if match:
        conf_hash = match.group(2)
        text = text.replace(match.group(0), '')
    else:
        conf_hash = None
    return conf_hash, text
