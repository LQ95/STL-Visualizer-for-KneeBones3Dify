

import assimp_py


post_flags = (assimp_py.Process_CalcTangentSpace)


  
#very minimal auxiliary class that is used to load STL models
class STLloader:
    model=[]
       
        
        
  
    #load stl file detects if the file is a text file or binary file
    def load_stl(self,filename):
        #read start of file to determine if its a binay stl file or a ascii stl file
        self.model = assimp_py.ImportFile(filename, post_flags)
  





    
#main program loop that can be used for tests

def main():


    model1=STLloader()
    
    model1.load_stl('C:\\Users\\mrapo\\AppData\\Local\\Temp\\MRI.stl')

    


if __name__ == '__main__':
    
    main()
