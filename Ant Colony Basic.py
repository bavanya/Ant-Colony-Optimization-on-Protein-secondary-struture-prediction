import numpy as np
import random

def read_train_file():
    f = open('RS126.csv','r')
    sentences = []
    tags = []
    sentence = []
    tag = []
    for line in f:
        s = line.rstrip('\n')
        
        n,w,t = line.split(',')
        sentence=list(w)
        tag=(list(t))[1:]
        #print(tag[:-1])
        sentences.append(sentence[:-1])
        tags.append(tag[:-1])
        sentence=[]
        tag=[]
    sentences = sentences[1:]
    tags = tags[1:]
    assert len(sentences) == len(tags)
    f.close()
    return (sentences,tags)

def next(arr, target, end): 
    start = 0;
  
    ans = -1
    while (start <= end): 
        mid = (start + end) // 2 
  
        # Move to right side if target is 
        # greater. 
        if (arr[mid] < target): 
            start = mid + 1
  
        # Move left side. 
        else: 
            if(mid==0 or arr[mid-1]<target):
                return mid
            end = mid - 1
  
    return start

def ACO(primary, sst,a,b,t):
    M=20
    N=len(primary)
    D=3
    
    ##Generate M initial possible solutions randomly
    states=['C','E','H']
    x = np.full((M,N),'A')  #Solution Matrix
    c = np.full((N,3),0.0)  #concentration
    p = np.full((N,3),1/3)  #probability matrix
    fitness= np.full((M),0.0)
    
    for j in range(0,M):
        for i in range(0,N):
            x[j][i]=random.choice(states)
    
    cnt=0
    while (cnt!=40):
        cnt=cnt+1
        rho=a
        Q=b/M
        alpha=t
        beta=1
        ##Evaluate fitness values for all solutions
        for j in range(0,M):  #jth solution
            fitness[j]=0.0
            for i in range(0,N):  #ith decision variable of jth solution
                if(x[j][i]==sst[i]):
                    fitness[j]=fitness[j]+1
                    
        for j in range(0,M):
            fitness[j]=fitness[j]/N
        
        ##
        for i in range(0,N):
            for d in range(0,3):
                delta=0
                for j in range(0,M):
                    if(x[j][i]==states[d]):
                        delta+=Q*fitness[j]
                
                c[i][d]=(1-rho)*c[i][d]+delta
                p[i][d]=pow(c[i][d],alpha)
            
            ##Evaluate probability of possible value d to be selected
            denominator=0
            for d in range(0,3):
                denominator+=pow(c[i][d],alpha)
                
            for d in range(0,3):
                p[i][d]=p[i][d]/denominator
            for d in range(1,3):
                p[i][d]+=p[i][d-1]
                
        ##
        for j in range(0,M):
            for i in range(0,N):
                rand=random.uniform(0,1)
                idx=next(p[i],rand,3)
                x[j][i]=states[idx]
                
    ##while ended
    maxfit=0
    for i in range(0,M):
        if(fitness[maxfit]<fitness[i]):
            maxfit=i
    
    return x[maxfit];

#Driver Code
if __name__ == '__main__': 
    primary = read_train_file()[0]
    sst = read_train_file()[1]
    
    ans=[]
    fitness=0.0
    total=0.0
    count=0
    print('yes')
    #for test in range(0,len(sst)):
    a=random.uniform(0.3,1)
    b=random.uniform(1,30)
    t=random.uniform(0,2)
    print('hii')
    for line in range(len(primary)):
        temp=ACO(primary[line], sst[line],a,b,t)
        ans.append(temp)

        for i in range(len(sst[line])):
            total+=1.0
            if(sst[line][i]==temp[i]):
                fitness+=1.0
                    
        print(str(a) + ' ' + str(b) + ' ' + str(t))
        print('Accuracy is '+ str(fitness/total))
    