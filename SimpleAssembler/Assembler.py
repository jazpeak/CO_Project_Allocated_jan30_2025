def Rtype(input_file):

    opRtype = {"add": "0110011",
                "sub": "0110011", 
                "slt": "0110011", 
                "srl": "0110011", 
                "or" : "0110011", 
                "and": "0110011"}

    funct3_map = {"add":"000","sub":"000","mul":"001","and":"111","or":"110","srl":"101","slt":"010"}