from MetaClass import Clean
import re
import json
import pandas as pd

#co_list = pd.read_json('./Schema/Reference/InfoCodeToFullName.json').InfoCode.values.tolist()
def not_redundant_int(x):
    '''
    有些數字在做文字探勘時要去掉，但如果這些數字是公司的infocode則先不去掉
    '''
    try:
        x=int(x)
        return False
    except:return True
    #return False 代表是要被清掉的詞
    
class Clean(Clean):
    def Capitalize(self):
        self.Text = self.Text.upper()
        return self

    def Separate(self, gram=1):
        parts = self.Text.split(" ")
        self.Text = []
        for i in range(len(parts) + 1 - gram):
            text = ""
            for j in range(gram):
                if j < gram and j != 0:
                    text = text + " " + str(parts[i + j])
                else:
                    text = text + str(parts[i + j])
            self.Text.append(text)
        return self

    def DeletePunctuation(self
                          , punctuation=['HTTP[S]?://\S+',"'S", "S'",',', '\.', '-', '"', "'",":",";",'!','‘','\$','&','/','\(','\)','\?','…','’','“','\=']
                          ):
        mid = self.Text
        for puncs in punctuation:
          mid = mid.encode('ascii',errors='ignore').decode('ascii')
          mid = re.sub(puncs, '', mid)
        resultwords = re.split(" \W+ ", mid)
        self.Text = " ".join(resultwords)
        return (self)
    

    def DeleteRedundant_Twitters(self):
        words=['A', 'THE', 'AN', 'TO', 'AND', 'OR', 'NOT','HE','HE','SHE','HIS','HER','THEM','THEY','BACK',
               'WANT','RIGHT','LEFT','WITHOUT','WITH','THEM','OF','AS','IN','MORE','FOR','ARE','IS','NEW','WILL','BE','AFTER',
               'WANTS', 'KNOW', 'HE', 'HISTORY', 'NAMES', 'TOO', 'RUN', 'NEEDS', 'WEEK', 'ANOTHER', 'GETTING', 'ON','BUT','COULD',
               'OUT','AT','THAN','HAVE','BY','WHAT','CAN','NOW','OVER','IT','ABOUT','MAY','HAS','HAVE','THEIR','QUARTER','DUE','UP','ITS',
               'YOU','YOUR','ENEN','WHY','HOW','THAT','THERE','THESE','NO','BEFORE','DO','DID','DONE','DOING','DONT','WAS','WERE',
               'LOOK','DON’T','ALL','INTO','ONTO','AROUND','TOWARDS','FROM','REVIEW','EUROPE','NORTH','GOVERNMENT','EXPERT',''
               'LEAD', 'NEED', 'GOES', 'BEHIND', 'GROUP', 'NEAR', 'WORKING', 'METOO', 'IF', 'GETS', 'GO', 'COMES', 'WHEN', 'THERE', 
               'PUT', 'USE', 'GOING', 'TALKS', 'WE', 'THEY', 'LIKELY', 'I', 'MONTH', 'OUR', 'PLAY', 'OWN', 'MY', 'MAKES', 'AD', 
               'AWAY', 'OFF', 'MUCH', 'LIVE', 'TV', 'NEARLY', 'DURING', 'BRING', 'PLAN', 'YIELD', 'WIN', 'FINALLY', 'TRY', 'AMONG', 
               'TAKING', 'WHERE', 'MADE', 'BUILD', 'TIES', 'HERE', 'THINK', 'YET', 'BOYS', 'RULES', 'NEXT', 'LESS', 'PART',
               'LEAVES', 'ASKS', 'NEWS', 'JUST', 'LOOKS', 'BEYOND', 'LATEST', 'KEY', 'MOVE', 'THIS', 'FINDS', 'THOSE', 'LITTLE', 
               'LIKE', 'BEEN', 'TODAY', 'NOTHING', 'HER', 'ALMOST', 'HAD', 'COMING', 'EDGES', 'FIRST', 'READ', 'AGAIN', 'DAY', 
               'WEAK', 'BETTER', 'LET', 'BETWEEN', 'GROWING', 'TAKE', 'LEARN', 'MONTHS', 'BEING', 'YEAR', 'MINUTES', 
               'RUNNING', 'RECORD', 'QUESTION', 'VS', 'WOULD', 'TOP', 'WAY', 'MANY', 'PEOPLE', 'HIS', 'EASY', 'SOME', 
               'ACROSS', 'DRIVE','WANT','NEED','GET','TALK','MAKE','US','CHINA','BIG','YORK','WORLD','MILLION',
               'WHITE','MARKET','MARKETS','TIME','AMERICA','UK','MAN','WOMAN','MEN','WOMEN','CAN’T','TWO','AMID','KEEP','END','HELP',
               'YEARS','LIFE','HIT','3RD','VERY',
               'YES','ASK','OTHERS','SOMETHING','ANYONE','EVERYONE','60M...','SO','BOTH','WANTED','YOURS','GUY','SAME','LOVES','GOING','DOES',
               'TRUE','EPIC','FOOT','REASONS','WASNT','DOG','11%','WEEKS','HANDS'
               'SINCE','SAID','WHICH','MYSELF','YOURSELF','HISSELF','HERSELF','THEMSELVES','NOPE','ALSO',
               'ANY','ME','SAY','ONE','SEE','RT','WHO','SHOULD','LIST','REAL','MIGHT','FEW','IM','NOR','REALLY','MOST','OTHER','ONLY','OKAY','ALONG',
               'ONCE','SEEMS','ACTUALLY','REVIEWS','FATHER','VIA','STILL','WE','MINE','ISNT','AINT','SAYS','EVER','CANNOT','THOUGH','LAST','SURE','THING',
               'DOOR','TRYING','NICE','ALWAYS','USUALLY','SOMETIMES','SELDOM','NEVER','REMEMBER','EVERY','GOT','ENOUGH','HIM','HER','HIS',
               'AM','WOULD','WOULDNT','OFTEN','TOTAL','AGE','SOON','BECAUSE','WO','DAYS','THERE','THERES','THEIR','COLUMN','ABLE','YEP','THATS','GONE','EXAMPLE',
               'THER','REASON','CHART','WONT','KNOWS','KNOW','TAKES','TOOK','DIFFERENT','DIFFERENCE','CAUSE','LISTEN','SUCH','HEAR','SIMILAR','HEY','HI','CONSTANT','EVEN','CASES',
               'SMART','DEGINITELY','READING','MATH','NAME','STREET','YOURE','ASKED','USING','WHOSE','ABSOLUTE','ABSOLUTELY','CAME','WHILE','FIGURE','GIRL','TALKING',
               'SPORTING','NIGHT','PERHAPS','USED','GIVE','THINKS','ONES','HEART','MOSTLY','ACTING','THANK','THANKS','THOUGHT','PLEASE','SAW','ABOVE','WHATS','MAYBE',
               'FUNNY','LEAST','LINK','DAILY','WORK','OH','CHILD','DOZEN','EACH','HELPS','FAVOTITE','STORY','IVE','MORNING','WEVE','HOUR',
               'SORRY','EST','ELSE','@DAVIDTAGGART','BUTTON','@JOHNPGAVIN','WENT','THROUGH','ENTRY','@BGURLEY','BIBLE','TOLD','TELL','MEANWHILE','ANYTHING','ANYWHERE',
               'PROBABLY','QUITE','SOURCES','STUDIES','LOVE','CANT','WOW','PAPER','CHOICE','GONNA','TYPE','SISTER','GUYS','FILES','STATION','EXERCISE',
               'WEEKEND','LOOKING','FULLY','HEARD','BUSY','HAHA','LOTS','RAN','RUN','HOURS','TWEETS','FIND','INSTEAD','AH','ATWELL','WEBSITE','SUMMARY','THUS','SEEM',
               'ADD','GAME','LEAVE','LISTED','USES','IDEA','YEAH','AHEAD','APPEARS','WAIT','SPEECH','TH','FINT','HOLDERS','WTF','BA','#2','HES','SIT',
               'FAR','FINE','DC','ID','8K','PRETTY','SHOW','SHOWS','READY','DIDNT','HAVING','SLAP','THINGS','OMG','YOY','IMEDIATELY','THEYRE','Q4','@EJENK','HAVENT','TWITTER',
               'CAREER','BURIED','RUNS','DEC','ACTUAL','CALL','UNTIL','RIP','PEERS','PICTURE','YY','HOWEVER'
               ]
        resultwords = [word for word in re.split("\s+", self.Text) if word.upper() not in words and len(word)>1 and not_redundant_int(word)]
        self.Text = " ".join(resultwords)
        return (self)


    def DeleteRedundant_News(self):
        words=['A', 'THE', 'AN', 'TO', 'AND', 'OR', 'NOT','HE','HE','SHE','HIS','HER','THEM','THEY','BACK',
               'WANT','RIGHT','LEFT','WITHOUT','WITH','THEM','OF','AS','IN','MORE','FOR','ARE','IS','NEW','WILL','BE','AFTER',
               'WANTS', 'KNOW', 'HE', 'HISTORY', 'NAMES', 'TOO', 'RUN', 'NEEDS', 'WEEK', 'ANOTHER', 'GETTING', 'ON','BUT','COULD',
               'OUT','AT','THAN','HAVE','BY','WHAT','CAN','CANT','NOW','OVER','IT','ABOUT','MAY','HAS','HAVE','THEIR','QUARTER','DUE','UP','ITS',
               'YOU','YOUR','ENEN','WHY','HOW','THAT','THERE','THESE','NO','BEFORE','DO','DID','DONE','DOING','DONT','WAS','WERE',
               'LOOK','DON’T','ALL','INTO','ONTO','AROUND','TOWARDS','FROM','REVIEW','EUROPE','NORTH','GOVERNMENT','EXPERT',''
               'LEAD', 'NEED', 'GOES', 'BEHIND', 'GROUP', 'NEAR', 'WORKING', 'METOO', 'IF', 'GETS', 'GO', 'COMES', 'WHEN', 'THERE', 
               'PUT', 'USE', 'GOING', 'TALKS', 'WE', 'THEY', 'LIKELY', 'I', 'MONTH', 'OUR', 'PLAY', 'OWN', 'MY', 'MAKES', 'AD', 
               'AWAY', 'OFF', 'MUCH', 'LIVE', 'TV', 'NEARLY', 'DURING', 'BRING', 'PLAN', 'YIELD', 'WIN', 'FINALLY', 'TRY', 'AMONG', 
               'TAKING', 'WHERE', 'MADE', 'BUILD', 'TIES', 'HERE', 'THINK', 'YET', 'BOYS', 'RULES', 'NEXT', 'LESS', 'PART',
               'LEAVES', 'ASKS', 'NEWS', 'JUST', 'LOOKS', 'BEYOND', 'LATEST', 'KEY', 'MOVE', 'THIS', 'FINDS', 'THOSE', 'LITTLE', 
               'LIKE', 'BEEN', 'TODAY', 'NOTHING', 'HER', 'ALMOST', 'HAD', 'COMING', 'EDGES', 'FIRST', 'READ', 'AGAIN', 'DAY', 
               'WEAK', 'BETTER', 'LET', 'BETWEEN', 'GROWING', 'TAKE', 'LEARN', 'MONTHS', 'BEING', 'YEAR', 'MINUTES', 
               'RUNNING', 'RECORD', 'QUESTION', 'VS', 'WOULD', 'TOP', 'WAY', 'MANY', 'PEOPLE', 'HIS', 'EASY', 'SOME', 
               'ACROSS', 'DRIVE','WANT','NEED','GET','TALK','MAKE','US','CHINA','BIG','YORK','WORLD','MILLION',
               'WHITE','MARKET','MARKETS','TIME','AMERICA','UK','MAN','WOMAN','MEN','WOMEN','CAN’T','TWO','AMID','KEEP','END','HELP',
               'YEARS','LIFE','HIT','YES','ASK','WHICH','WHO','HOME','SAYS','SAY','STOCK','STOCKS','GOOD','PUSH','ONE','SUPER','INVESTORS',
               'INVESTOR','POWER','CITY','CALL','CALLS','BILLION','MILLION','WATCH','LOVE','ISNT','ARENT','WERENT','ANYTHING','EVERYTHING',
               'GIVE','THINKS','HES','JAN','FIVE','COURT',''
               
               ]
        resultwords = [word for word in re.split("\s+", self.Text) if word.upper() not in words and len(word)>1 and not_redundant_int(word)]
        self.Text = " ".join(resultwords)
        return (self)



    def Close(self):
      print(self.Text)
      return self



