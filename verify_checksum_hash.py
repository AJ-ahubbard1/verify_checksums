import io, hashlib, hmac
BLOCKSIZE = 65536
file = 'manjaro-kde-22.0.2-230203-linux61.iso'
checkfile = file + ".sha1"
def getHash():
  algorithm = input("Enter hash type: [sha1 | sha224 | sha256 | sha512 | md5]\n")

  if algorithm == 'sha1':
    return hashlib.sha1()
  elif algorithm == 'sha224':
    return hashlib.sha224()
  elif algorithm == 'sha256':
    return hashlib.sha256()
  elif algorithm == 'sha512':
    return hashlib.sha512()
  elif algorithm == 'md5':
    return hashlib.md5()
  else:
    print("error: hash type not found!")
    return getHash()

h = getHash()

def hashFile(hash, filename):
  with open(filename, 'rb') as afile:
    buf = afile.read(BLOCKSIZE)
    while len(buf) > 0:
      hash.update(buf)
      buf = afile.read(BLOCKSIZE)
      hash.hexdigest()
    return hash.hexdigest()

hashValue = hashFile(h, file)

checkSum =  open(checkfile,"r")
print(str(hashValue))
print(str(hashValue) in checkSum.read())
