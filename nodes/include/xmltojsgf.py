import collections
import xml.etree.ElementTree as ET

def xml_to_grammar(filename):
	tree = ET.parse(filename)
	root = tree.getroot()
	grammar = open(filename.replace('xml','jsgf'),'w+')
	grammar.write('#JSGF V1.0;\n')
	grammar.write('grammar ' + root.attrib['name'] + ';\n');

	for child in root:
		if child.tag == 'rule':
			line = ('public ' if child.attrib['public'] == 'true' else '') + '<%s> = ' % child.attrib['name']
			for subchild in child:
				line += ('<%s>' % subchild.attrib['name']) + '|'
			grammar.write(line[0:len(line)-1]+';\n')
		elif child.tag == 'words':
			line = '<%s> = ' % child.attrib['name']
			for subchild in child:
				line += subchild.text + '|'
			grammar.write(line[0:len(line)-1]+';\n')
	grammar.close()

def get_word_list(filename):
	tree = ET.parse(filename)
	root = tree.getroot()
	words = []
	for child in root:
		if child.tag == 'words':
			for subchild in child:
				words.append(subchild.text)
	return words

def create_weight_grammar(xmlfile,weight):
	tree = ET.parse(xmlfile)
	root = tree.getroot()
	grammar = open(xmlfile.replace('xml','jsgf'),'w+')
	grammar.write('#JSGF V1.0;\n')
	grammar.write('grammar ' + root.attrib['name'] + ';\n');

	for child in root:
		if child.tag == 'rule':
			line = ('public ' if child.attrib['public'] == 'true' else '') + '<%s> = ' % child.attrib['name']
			for subchild in child:
				line += ('<%s>' % subchild.attrib['name'])
				if child.attrib['conj'] == 'or':
					line += '|'
				elif child.attrib['conj'] == 'none':
					line += ' '
			grammar.write(line[0:len(line)-1]+';\n')
		elif child.tag == 'words':
			line = '<%s> = ' % child.attrib['name']
			for subchild in child:
				line += ('/%f/' % weight[subchild.text]) + subchild.text + '|'
			grammar.write(line[0:len(line)-1]+';\n')
	grammar.close()
