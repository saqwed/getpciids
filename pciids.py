import os, re
import git, chardet

pciids_repo = 'https://github.com/pciutils/pciids.git'
tmp_git_repo = '.tmp/'
pci_ids_raw_file = os.path.join(tmp_git_repo, 'pci.ids')

def checkEncoding(file):
    bytes = min(32, os.path.getsize(file))
    raw = open(file, 'rb').read(bytes)
    result = chardet.detect(raw)
    encoding = result['encoding']
    return encoding

try:
    # if the repository does not exist yet, clone it first
    new_repo = git.Repo.clone_from(url = pciids_repo, to_path = tmp_git_repo)
except:
    pass

with git.Repo.init(path=tmp_git_repo) as repo:
    # discard any changes
    repo.index.checkout(force=True)
    remote = repo.remote()
    # pull new changes
    remote.pull()

#===============================================================================
# Syntax:
# vendor  vendor_name
#	device  device_name				<-- single tab
#		subvendor subdevice  subsystem_name	<-- two tabs
#===============================================================================
# ^[0-9a-fA-F]{4}\s{2}.*
# ==> https://regex101.com/r/qYNtkz/1
# ^\t[0-9a-fA-F]{4}\s{2}.*
# ==> https://regex101.com/r/Lwfd8e/1
# ^\t{2}[0-9a-fA-F]{4}\s[0-9a-fA-F]{4}\s{2}.*
# ==> https://regex101.com/r/UW8TlF/1
#===============================================================================
# 0e11  Compaq Computer Corporation
# 	0001  PCI to EISA Bridge
# 	0002  PCI to ISA Bridge
# 	0046  Smart Array 64xx
# 		0e11 4091  Smart Array 6i
# 		0e11 409a  Smart Array 641
# 		0e11 409b  Smart Array 642
# 		0e11 409c  Smart Array 6400
# 		0e11 409d  Smart Array 6400 EM
#===============================================================================

list1 = []
list2 = []
list3 = []
pattern1 = re.compile(r"^[0-9a-fA-F]{4}\s{2}.*")
pattern2 = re.compile(r"^\t[0-9a-fA-F]{4}\s{2}.*")
pattern3 = re.compile(r"^\t{2}[0-9a-fA-F]{4}\s[0-9a-fA-F]{4}\s{2}.*")
# open the file with detected character encoding
for i, line in enumerate(open(pci_ids_raw_file, encoding = checkEncoding(pci_ids_raw_file), errors = 'ignore')):
    for match in re.findall(pattern1, line):
        line = re.sub('\s+',' ',line).strip() # replace multiple whitespaces with single spaces
        list1.append(line.split(' ', 1))
    for match in re.findall(pattern2, line):
        line = re.sub('\s+',' ',line).strip() # replace multiple whitespaces with single spaces
        list2.append(line.split(' ', 1))
    for match in re.findall(pattern3, line):
        line = re.sub('\s+',' ',line).strip() # replace multiple whitespaces with single spaces
        list3.append(line.split(' ', 2))

# print(len(list3))

for vendor, description in list1:
    # print(vendor)
    # print(description)
    if '8086' == vendor:
        print('Found: ' + description)
        break

for did, description in list2:
    # print(did)
    if '9a49' == did:
        print("Found: " + description)
        break

for svid, ssid, description in list3:
    # print(svid)
    if '06dc' == ssid:
        print("Found: " + description)
        break