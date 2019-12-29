from sklearn import tree
import csv
from SqliteHandler import SqliteHandler 
class ML:
    features = []
    label = []

    def __init__(self):
        sql = SqliteHandler()
        rows = sql.get_all_items('Follower', False)
        for row in rows:
            x = []
            x.append(row[3]) # Private
            x.append(row[4]) # Following (If you follow that user)
            x.append(row[6]) # Follower ratio
            x.append(row[7]) # Tag ratio
            x.append(row[8]) # Activity ratio      

            self.label.append(row[5])
            self.features.append(x)

    def execute(self, json_user):
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(self.features, self.label)

        #1306804065,enana_ariii,𝑨𝒓𝒊𝒂𝒅𝒏𝒂 𝑹𝒐𝒔𝒂😈,1,1,1,1.6741463414634146,0.0,0.15833223380393194
        result = clf.predict([[json_user['is_private'], json_user['following'], json_user['follower_ratio'],\
             json_user['tag_ratio'], json_user['activity_ratio'], json_user['user_ratio']]])
        #result = clf.predict([[1,1,1.6741463414634146,0.15,0.15833223380393194]])
        return result[0]