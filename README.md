# voice_authentication
voice authentication module
    steps to use :
        1 - create folder with %person and create folders train and test inside it
        2 - add >=3 utterances of same sentence from below list of sentences into a wav
        file with 44100 sampling rate and length between 1.3s - 5s,
        
            1 - Hello I am very happy today
            2 - Never forget tomorrow is a new day	
            3 - Eventually winter will turn into spring	
            4 - Remember to wash your hands before eating	
            
        a trained sentence is one where 3 utterences are successfully registered
            
        3 - add >=1 utterences for testing in test folder(with same config as train wav)
        note - test must be from the trained sentences only.
        4 - change the %workdir to where you store the folder
        5 - give user information in %user information section accordingly
