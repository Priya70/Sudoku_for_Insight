#/usr/bin/python
'''
A very basic sudoku solver taht seems to solve the "easy" puzzles and some "medium" ones.
It does not search and backtrack - just updates. and propogates.
usage: python sudoku.py  csv_file

'''
import logging
import sys


def create_grid():
    numbers=[1,2,3,4,5,6,7,8,9]
    #create a list of the keys for the dictionary which will hold all the values at each position of the sudku grid
    squares=[(a,b) for a in numbers for b in numbers]     
    return squares
    
def import_to_grid(squares,file):
    f=open(file,'r').read()
    #replace the \n at line ends with a ",", so I can plit on ","
    f=f.replace("\n",',')
    digits=f.split(',')
    grid=dict(zip(squares,digits))        
    return grid

def get_row(sqA, row_list):
    ''' function that gets the rest of the squares which are contained in the same sublist of row_list as sqA'''    
    for r in row_list:
        if sqA in r:
           return r 
    
def get_col(sqB,col_list):
    '''function that gets the rest of the squares which are contained in the same sublist of col_list as sqB '''
    for c in col_list:
        if sqB in c:            
            return c
       
def get_neighbors(sqA,neighbors_list):    
    '''function that gets the rest of the squares which are contained in the same sublist of neighbors _list as sqA  ''' 
    for n in neighbors_list:
        if sqA in n:
            return n

def update_sudoku_grid(sudoku_grid,row_list,col_list,neighbors_list): 
    for s, d in sudoku_grid.items():
        if len(d)>1:
            row_s=get_row(s, row_list) 
            row_values_s=[sudoku_grid[k] for k in row_s]
            col_s=get_col(s, col_list)
            col_values_s=[sudoku_grid[k] for k in col_s]
            neighbors_s= get_neighbors(s,neighbors_list) 
            neighbor_values_s=[sudoku_grid[k] for k in neighbors_s]
            union= set(row_values_s+col_values_s+neighbor_values_s)-set([d])
            tmp=[k for k in d if k not in list(union)]
            if len(tmp)>1:
                sudoku_grid[s]=('').join(tmp)
            elif len(tmp)==1:
                sudoku_grid[s]=tmp[0]
            else:                    
                print "Error at square",s
                exit     
    print sudoku_grid          
    values=[d for s,d in sudoku_grid.items()] 
    for v in values:
        if len(v)>1:
            update_sudoku_grid(sudoku_grid,row_list,col_list,neighbors_list)  
        else:
            print "sudoku solved"
            return sudoku_grid

#[d for s,d in sudoku_grid.items()] # list of all values    
#[s for s,d in sudoku_grid.items() if d == '0'] 



def main(args):
    csv_file=args[1]
    squares=create_grid()
    #sys.argv[1]='sudoku_test1.csv'
    sudoku_grid=import_to_grid(squares,csv_file)
    row_list=[[s for s in squares[0+(i*9):9+(i*9)] ]for i in range(0,9)]
    col_list=[[squares[j+9*i] for i in range(0,9)] for j in range(0,9)]
    #create a list of lists of neighbours
    neighbors_list=[[] for i in range(0,9)]
    for i in range(0,9):
         neighbors_list[i]=[squares[j] for j in range (0,81) if  ((j/27)*3 + (j%9/3) == i) ]  
    #Create a separate dictionary containing all possible values to squares in sudoku_grid where value is 0
    possible_values =dict((s,'123456789') for s in squares)
    #update all squares with value='0' to have possible values'123456789'
    for s, d in sudoku_grid.items():
        if d =='0': #ie d==0
            sudoku_grid[s]=possible_values[s]   
    res=update_sudoku_grid(sudoku_grid,row_list,col_list,neighbors_list)               
  
    

if __name__ == '__main__':
    if len(sys.argv) == 2:
        print "length is ", len(sys.argv)
        main(sys.argv) 

        