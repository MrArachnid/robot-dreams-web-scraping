import xml.etree.ElementTree as ET

def parse_xml_1():
    tree = ET.parse('cats.xml')
    root = tree.getroot()

    facts = []
    for child in root:
        # print(child.tag, child.attrib)
        for grandchild in child:
            if grandchild.tag == 'fact':
                facts.append(grandchild.text)

    print(facts)
    with open('cats.txt', 'w') as f:
        f.write('\n'.join(facts))

def parse_xml_2():        
    tree = ET.parse('cats.xml')
    root = tree.getroot()

    facts = []
    for info in root.findall('info'):
        fact = info.find('fact')
        facts.append(fact.text)

    print(facts)
    with open('cats.txt', 'w') as f:
        f.write('\n'.join(facts))


if __name__ == '__main__':
    parse_xml_2()