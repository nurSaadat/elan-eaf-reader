from xml.etree import cElementTree as etree
import pympi.Elan as Elan

def parse_eaf(file_path, eaf_obj):
    """Parse an EAF file
    :param str file_path: Path to read from, - for stdin.
    :param pympi.Elan.Eaf eaf_obj: Existing EAF object to put the data in.
    :returns: EAF object.
    """
    if file_path == '-':
        file_path = sys.stdin
    # Annotation document
    try:
        tree_root = etree.parse(file_path).getroot()
    except etree.ParseError:
        raise Exception('Unable to parse eaf, can you open it in ELAN?')

    if tree_root.attrib['VERSION'] not in ['2.8', '2.7']:
        logging.warning('Parsing unknown version of ELAN spec... '
                    'This could result in errors...\n')
    eaf_obj.adocument.update(tree_root.attrib)
    del(eaf_obj.adocument['{http://www.w3.org/2001/XMLSchema-instance}noNamesp'
                          'aceSchemaLocation'])
    tier_number = 0
    for elem in tree_root:
        # Licence
        if elem.tag == 'LICENSE':
            eaf_obj.licenses.append((elem.text, elem.attrib['LICENSE_URL']))
        # Header
        if elem.tag == 'HEADER':
            eaf_obj.header.update(elem.attrib)
            for elem1 in elem:
                if elem1.tag == 'MEDIA_DESCRIPTOR':
                    eaf_obj.media_descriptors.append(elem1.attrib)
                elif elem1.tag == 'LINKED_FILE_DESCRIPTOR':
                    eaf_obj.linked_file_descriptors.append(elem1.attrib)
                elif elem1.tag == 'PROPERTY':
                    eaf_obj.properties.append(
                        (elem1.attrib['NAME'], elem1.text))
        # Time order
        elif elem.tag == 'TIME_ORDER':
            for elem1 in elem:
                tsid = elem1.attrib['TIME_SLOT_ID']
                tsnum = int(''.join(filter(str.isdigit, tsid)))
                if tsnum and tsnum > eaf_obj.maxts:
                    eaf_obj.maxts = tsnum
                ts = elem1.attrib.get('TIME_VALUE', None)
                eaf_obj.timeslots[tsid] = ts if ts is None else int(ts)
        # Tier
        elif elem.tag == 'TIER':
            tier_id = elem.attrib['TIER_ID']
            align = {}
            ref = {}
            for elem1 in elem:
                if elem1.tag == 'ANNOTATION':
                    for elem2 in elem1:
                        if elem2.tag == 'ALIGNABLE_ANNOTATION':
                            annot_id = elem2.attrib['ANNOTATION_ID']
                            annot_num = int(''.join(
                                filter(str.isdigit, annot_id)))
                            if annot_num and annot_num > eaf_obj.maxaid:
                                eaf_obj.maxaid = annot_num
                            annot_start = elem2.attrib['TIME_SLOT_REF1']
                            annot_end = elem2.attrib['TIME_SLOT_REF2']
                            svg_ref = elem2.attrib.get('SVG_REF', None)
                            align[annot_id] = (annot_start, annot_end,
                                               '' if not list(elem2)[0].text
                                               else list(elem2)[0].text,
                                               svg_ref)
                            eaf_obj.annotations[annot_id] = tier_id
                        elif elem2.tag == 'REF_ANNOTATION':
                            annot_ref = elem2.attrib['ANNOTATION_REF']
                            previous = elem2.attrib.get('PREVIOUS_ANNOTATION',
                                                        None)
                            annot_id = elem2.attrib['ANNOTATION_ID']
                            annot_num = int(''.join(
                                filter(str.isdigit, annot_id)))
                            if annot_num and annot_num > eaf_obj.maxaid:
                                eaf_obj.maxaid = annot_num
                            svg_ref = elem2.attrib.get('SVG_REF', None)
                            ref[annot_id] = (annot_ref,
                                             '' if not list(elem2)[0].text else
                                             list(elem2)[0].text,
                                             previous, svg_ref)
                            eaf_obj.annotations[annot_id] = tier_id
            eaf_obj.tiers[tier_id] = (align, ref, elem.attrib, tier_number)
            tier_number += 1
        # Linguistic type
        elif elem.tag == 'LINGUISTIC_TYPE':
            eaf_obj.linguistic_types[elem.attrib['LINGUISTIC_TYPE_ID']] =\
                elem.attrib
        # Locale
        elif elem.tag == 'LOCALE':
            eaf_obj.locales[elem.attrib['LANGUAGE_CODE']] =\
                (elem.attrib.get('COUNTRY_CODE', None),
                 elem.attrib.get('VARIANT', None))
        # Language
        elif elem.tag == 'LANGUAGE':
            eaf_obj.languages[elem.attrib['LANG_ID']] =\
                (elem.attrib.get('LANG_DEF', None),
                 elem.attrib.get('LANG_LABEL', None))
        # Constraint
        elif elem.tag == 'CONSTRAINT':
            eaf_obj.constraints[elem.attrib['STEREOTYPE']] =\
                elem.attrib['DESCRIPTION']
        # Controlled vocabulary
        elif elem.tag == 'CONTROLLED_VOCABULARY':
            cv_id = elem.attrib['CV_ID']
            ext_ref = elem.attrib.get('EXT_REF', None)
            descriptions = []

            if 'DESCRIPTION' in elem.attrib:
                eaf_obj.languages['und'] = (
                    'http://cdb.iso.org/lg/CDB-00130975-001',
                    'undetermined (und)')
                descriptions.append(('und', elem.attrib['DESCRIPTION']))
            entries = {}
            for elem1 in elem:
                if elem1.tag == 'DESCRIPTION':
                    descriptions.append((elem1.attrib['LANG_REF'], elem1.text))
                elif elem1.tag == 'CV_ENTRY':
                    cve_value = (elem1.text, 'und',
                                 elem1.get('DESCRIPTION', None))
                    entries['cveid{}'.format(len(entries))] = \
                        ([cve_value], elem1.attrib.get('EXT_REF', None))
                elif elem1.tag == 'CV_ENTRY_ML':
                    cem_ext_ref = elem1.attrib.get('EXT_REF', None)
                    cve_id = elem1.attrib['CVE_ID']
                    cve_values = []
                    for elem2 in elem1:
                        if elem2.tag == 'CVE_VALUE':
                            cve_values.append((elem2.text,
                                               elem2.attrib['LANG_REF'],
                                               elem2.get('DESCRIPTION', None)))
                    entries[cve_id] = (cve_values, cem_ext_ref)
            eaf_obj.controlled_vocabularies[cv_id] =\
                (descriptions, entries, ext_ref)
        # Lexicon ref
        elif elem.tag == 'LEXICON_REF':
            eaf_obj.lexicon_refs[elem.attrib['LEX_REF_ID']] = elem.attrib
        # External ref
        elif elem.tag == 'EXTERNAL_REF':
            eaf_obj.external_refs[elem.attrib['EXT_REF_ID']] = (
                elem.attrib['TYPE'], elem.attrib['VALUE'])

def change_function():
    Elan.parse_eaf = parse_eaf