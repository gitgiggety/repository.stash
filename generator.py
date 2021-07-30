import sys
import os
import xml.etree.ElementTree
import zipfile
import hashlib

def parse_zip(addon_id, version):
    path = os.path.join(addon_id, '{}-{}.zip'.format(addon_id, version))

    with zipfile.ZipFile(path, 'r') as zip:
        with zip.open(os.path.join(addon_id, 'addon.xml')) as addon_file:
            try:
                tree = xml.etree.ElementTree.parse(addon_file)
            except IOError:
                raise RuntimeError('Cannot open add-on metadata: {}'.format(addon_file))

            root = tree.getroot()

            return root

def update_addons(addon_metadata):
    with open('addons.xml', 'rb') as addons_file:
        addons = xml.etree.ElementTree.parse(addons_file)

        root = addons.getroot()
        addon_element = root.find('addon[@id="{}"][@versiom="{}"]'.format(addon_metadata.get('id'), addon_metadata.get("version")))
        if addon_element != None:
            root.remove(addon_element)

        root.insert(0, addon_metadata)

    with open('addons.xml', 'wb') as addons_file:
        addons.write(addons_file, encoding='UTF-8', xml_declaration=True)

def update_checksum():
    checksum = hashlib.md5()
    with open('addons.xml', 'rb') as addons_file:
        for chunk in iter(lambda: addons_file.read(2**12), b''):
            checksum.update(chunk)
    digest = checksum.hexdigest()

    with open('addons.xml.md5', 'w', newline='\n') as checksum_file:
        checksum_file.write(u'{}  {}\n'.format(digest, 'addons.xml'))

if __name__ == "__main__":
    addon = parse_zip(sys.argv[1], sys.argv[2])
    update_addons(addon)
    update_checksum()
