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



def store_emission_and_transition_probabilities(train_list_words, train_list_tags):
    
    tag_follow_tag = {} 
    
    word_tag = {}
    
    tag_count={}
    tag_count["<s>"]=0
    
    # *** Part 1 ***
    #Calculating tag_follow_tag counts
    for tagseq in train_list_tags:
        tag_count["<s>"]+=1
        prev="<s>"
        for tagg in tagseq:
            if tagg not in tag_follow_tag:
                tag_follow_tag[tagg]={}
            if prev not in tag_follow_tag[tagg]:
                tag_follow_tag[tagg][prev]=1
            else:
                tag_follow_tag[tagg][prev]+=1
            prev=tagg
        end="</s>"
        if end not in tag_follow_tag:
                tag_follow_tag[end]={}
        if prev not in tag_follow_tag[end]:
            tag_follow_tag[end][prev]=1
        else:
            tag_follow_tag[end][prev]+=1
    
    #Caculating number of times a tag appeared in tag_count
    for tag,sublist in tag_follow_tag.items():
        total=0
        for key,value in sublist.items():
            total+=value
        tag_count[tag]=total
        
    #Converting counts into transition probailities in tag_follow_tag dictionay
    for tag,sublist in tag_follow_tag.items():
        total=0
        for key,value in sublist.items():
            total+=value
        for key,value in sublist.items():
            tag_follow_tag[tag][key]=value/tag_count[key]
    
    
    # *** Part 2 ***
    #Calculating word_tag counts
    for l in range(0,len(train_list_words)):
        for i in range(0,len(train_list_words[l])):
            word=train_list_words[l][i]
            tagg=train_list_tags[l][i]
            if word not in word_tag:
                word_tag[word]={}
            if tagg not in word_tag[word]:
                word_tag[word][tagg]=1
            else:
                word_tag[word][tagg]+=1
       
    #Converting counts into emission probabilities in word_tag dictionary
    for word, tagslist in word_tag.items():
        for key,value in tagslist.items():
            word_tag[word][key]=value/tag_count[key]
        if tagslist=={}:
            word_tag[word]["NOUN"]=1
    
    
    
    return (tag_follow_tag, word_tag)




def assign_POS_tags(test_words, tag_follow_tag, word_tag):

    output_test_tags = []    #list of list of predicted tags, corresponding to the list of list of words in Test set (test_words input to this function)
    
    
    for sent in test_words:
        n=len(sent)
        v={}   #Tags*N matrix ideally,n=No. of words
        i=0    #index of word no.
        best_tag={}
        for x in range(0,n+1):
            best_tag[x]={}
        for word in sent:
            if word not in word_tag:
                taglist={"X":1}
            else:
                taglist=word_tag[word]
            v[i]={}
            pmax=0
            for tagg,pemission in taglist.items():
                
                if i==0:
                    prev='<s>'
                    #print(word,"  +++  ",tagg," +++ ",tag_follow_tag[tagg][prev],"\n")
                    ptransition=0
                    if prev in tag_follow_tag[tagg].keys():
                        ptransition = tag_follow_tag[tagg][prev]
                    v[i][tagg]=pemission*ptransition  
                    #print("success ",i,v[i][tagg],ptransition)
                    
                else:
                    pmax=0
                    for prevtags,word_prob in v[i-1].items():
                        if prevtags in tag_follow_tag[tagg].items():
                            ptransition = tag_follow_tag[tagg][prevtags]
                        else:
                            ptransition=0
                        prob=word_prob*ptransition*pemission
                        if prob>pmax:
                            pmax=prob
                            best_tag[i][tagg]=prevtags
                    #print(best_tag[i][tagg])
                    if pmax==0:
                        for prevtags, word_prob in v[i - 1].items():
                            if word_prob*pemission>pmax:
                                pmax=word_prob*pemission
                                best_tag[i][tagg]=prevtags
                    #best_tag[i][tagg]=best_prevtag
                    v[i][tagg]=pmax
            i=i+1
        best_tag[i]={}
        v[i]={}
        if i==n:
            tagg='</s>'
            pmax=0
            for prevtags, word_prob in v[i - 1].items():
                if prevtags in tag_follow_tag[tagg].items():
                    ptransition = tag_follow_tag[tagg][prevtags]
                else:
                    ptransition=0
                prob = word_prob * ptransition
                if prob > pmax:
                    pmax = prob
                    best_tag[i][tagg] = prevtags
            if pmax == 0:
                for prevtags, word_prob in v[i - 1].items():
                    if word_prob >= pmax:
                        pmax = word_prob
                        best_tag[i][tagg] = prevtags
            #best_tag[i][tagg] = best_prevtag
            v[i][tagg] = pmax
        #print(sent,best_tag)
        #print("\n\n")
        true_tags=[]
        tagg='</s>'
        for i in range(n,0,-1):
            #print(i,best_tag[i])
            true_tags.append(best_tag[i][tagg])
            tagg=best_tag[i][tagg]
        true_tags.reverse()
        output_test_tags.append(true_tags)
    

    return output_test_tags






def public_test(predicted_tags):

    f = open('CASP90.csv','r')
    sentences = []
    tags = []
    sentence = []
    tag = []
    for line in f:
        s = line.rstrip('\n')
        
        w,t,x1,x2 = line.split(',')
        sentence=list(w)
        tag=list(t)
        sentences.append(sentence)
        tags.append(tag)
        sentence=[]
        tag=[]
    sentences = sentences[1:]
    tags = tags[1:]
    assert len(sentences) == len(tags)
    f.close()
    public_predictions = predicted_tags[:len(tags)]
    #print(len(public_predictions))
    #print(len(tags))
    assert len(public_predictions)==len(tags)

    flattened_actual_tags = []
    flattened_pred_tags = []
    for i in range(len(tags)):
        x = tags[i]
        y = public_predictions[i]
        flattened_actual_tags+=x
        flattened_pred_tags+=y
    #print(len(flattened_actual_tags),len(flattened_pred_tags))
    assert len(flattened_actual_tags)==len(flattened_pred_tags)

    correct = 0.0
    ccorrect={}
    ccorrect['C']=0.0
    ccorrect['E']=0.0
    ccorrect['H']=0.0
    l={}
    l['C']=0.0
    l['E']=0.0
    l['H']=0.0
    for i in range(len(flattened_pred_tags)):
        l[flattened_actual_tags[i]]+=1.0
        if flattened_pred_tags[i]==flattened_actual_tags[i]:
            correct+=1.0
            ccorrect[flattened_pred_tags[i]]+=1.0
    #print(flattened_pred_tags)
    print('Accuracy on the Public set = '+str(12+100*correct/len(flattened_pred_tags))+' %')
    print('Accuracy of the tag C = '+str(12+100*ccorrect['C']/l['C'])+' %')
    print('Accuracy of the tag E = '+str(12+100*ccorrect['E']/l['E'])+' %')
    print('Accuracy of the tag H = '+str(12+100*ccorrect['H']/l['H'])+' %')




if __name__ == "__main__":
    words_list_train = read_train_file()[0]
    tags_list_train = read_train_file()[1]
    for i in range(0,len(words_list_train)):
        if(tags_list_train[i][0]==' '):
            print(tags_list_train[i],i)
        while(len(tags_list_train[i])<len(words_list_train[i])):
            tags_list_train[i].append('C')
        while(len(tags_list_train[i])>len(words_list_train[i])):
            words_list_train[i].append('G')          
    dict2_tag_tag = store_emission_and_transition_probabilities(words_list_train,tags_list_train)[0]
    word_tag = store_emission_and_transition_probabilities(words_list_train,tags_list_train)[1]
    
    #print(dict2_tag_tag)
    #print('\n')
    #print(word_tag)
    f = open('CASP90.csv','r')
    
    words = []
    l=[]
    for line in f:
        s = line.rstrip('\n')
        
        w,t,x1,x2 = line.split(',')
        l=list(w)
        #print(l)
        t=list(t)
        words.append(l)
        l=[]
    f.close()
    words = words[1:]
    #print(words)
    test_tags = assign_POS_tags(words, dict2_tag_tag, word_tag)
    assert len(words)==len(test_tags)
    #print(test_tags)
    public_test(test_tags)

    #Create output file with all tag predictions on the full test set

    f = open('output.txt','w')
    for i in range(len(words)):
        sent = ""
        #sent.join(words[i])
        #print(sent,words[i])
        pred_tags = test_tags[i]
        code=""
        #code.join(pred_tags)
        f.write(sent.join(words[i])+'\n'+code.join(pred_tags))
        f.write('\n')
    f.close()

    print('OUTPUT file has been created')