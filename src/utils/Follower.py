
import json
import re 

class Follower:
    """
    parametros: ratio followers, ratio tags, fecha last foto, ratio actividad, num fotos.
    """
    username = ""
    pk = ""
    full_name = ""
    is_private = ""
    following = False
    followed_by = False
    follower_ratio = ""
    tag_ratio = ""
    activity_ratio = ""
    user_ratio = ""

    #coming from configs
    api = ""
    tags = ""

    def __init__(self, user_json, api, tags, users):
        self.username = user_json['username']
        self.pk = user_json['pk']
        if user_json['full_name'] is '':
            self.full_name = 'None'
        else:
            self.full_name = user_json['full_name']
        self.is_private = user_json['is_private']
        self.api = api
        self.tags = tags
        self.users = users

        # meethod calls
        self.user_ratio_ratio()
        self.tag_ratio_method()
        self.check_following_status()
        self.is_private_method(user_json['is_private'])
        self.follower_ratio_method()

    def user_ratio_ratio(self):
        count = 0
        next_max_id = True
        while next_max_id:
            if next_max_id is True:
                next_max_id = ''
                try:    
                    _ = self.api.getUserFollowings(self.pk, maxid=next_max_id)
                    users = self.api.LastJson['users']
                except Exception as e:
                    print(e)
                    count = -1
                    break
                for user in users:
                    if user['username'] in self.users:
                        count += 1
        next_max_id = self.api.LastJson.get('next_max_id', '')
        self.user_ratio = count/len(self.users)


    def tag_ratio_method(self):
        count = 0
        comment_count = 0
        like_count = 0
        next_max_id = True
        while next_max_id:
            if next_max_id is True:
                next_max_id = ''
            try:
                self.api.getUserFeed(self.pk, next_max_id)
                items = self.api.LastJson['items']
            except Exception as e:
                print(e)
            for photo in items:
                try:
                    comment_count += int(photo['comment_count'])
                    like_count += int(photo['like_count'])
                except KeyError: #Picture might not have likes or comments
                    pass
                try:
                    words = photo['caption']['text'].split("#")
                except TypeError:
                    words = []
                for word in words:
                    if word.strip(' ') in self.tags:
                        count += 1
            next_max_id = self.api.LastJson.get('next_max_id', '')
        try:
            # numero de tags coicidentes / numero de tags nuestros * numero de fotos
            self.tag_ratio = count/(len(self.tags)*len(self.api.LastJson['items']))
            # 
            self.activity_ratio = (len(self.api.LastJson['items'])/(comment_count + like_count))*100
        except ZeroDivisionError:
            self.tag_ratio= 0
            self.activity_ratio = 0
        except KeyError as e:
            print(e)
            self.tag_ratio = -1
            self.activity_ratio = -1
        return
    

    def follower_ratio_method(self):
        self.api.getUsernameInfo(self.pk)
        try:
            self.follower_ratio = int(self.api.LastJson['user']['follower_count'])/int(self.api.LastJson['user']['following_count'])
            #print(self.follower_ratio)
        except ZeroDivisionError:
            self.follower_ratio = 0
        except:
            self.follower_ratio = -1
        return

    def is_private_method(self, is_private):
        if is_private:
            self.is_private = 1
        else:
            self.is_private = 0
        return

    def check_following_status(self):
        try:
            print(self.api.userFriendship(self.pk))
        except:
            self.following = -1
            self.followed_by = -1
        try:
            self.following = self.api.LastJson['following']
        except:
            self.following = -1
        try:
            self.followed_by = self.api.LastJson['followed_by']
        except Exception as e:
            print(e)
            self.followed_by = -1
        return

    def get_user(self):
        user = {
            "username": self.username,
            "pk": self.pk,
            "full_name": self.full_name,
            "is_private": self.is_private,
            "following": self.following, 
            "followed_by": self.followed_by,
            "follower_ratio":str(self.follower_ratio),
            "tag_ratio": str(self.tag_ratio),
            "activity_ratio": str(self.activity_ratio),
            "user_ratio": str(self.user_ratio)
        }
        return user

