import sys
import base64

def main():
	
	if len(sys.argv) != 3:
		print("python encode.py [username] [password]")
		return
		
	username = sys.argv[1]
	password = sys.argv[2]

	base = str(username) + ":" + str(password) 
	print(base64.b64encode(base.encode("utf-8")).decode("utf-8"))
	return

if __name__ == '__main__':
	main()	
