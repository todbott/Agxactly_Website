import oauth2 as oauth
import requests
import json
import os

consumer_key = '86fm0w2bz314ep' #from Linkedin site
consumer_secret = '6jnLiofYfmgcJPRh' #from Linkedin site
consumer = oauth.Consumer(consumer_key, consumer_secret)
client = oauth.Client(consumer)

def getAuthCode():
    request_authorizationCode_url = 'https://www.linkedin.com/oauth/v2/authorization'
    payload = {'response_type': 'code', 'client_id': consumer_key, 'redirect_uri': 'http://www.agxactly.com', 'state': 'hey', 'scope': 'w_member_social,r_liteprofile'}
    r = requests.get(request_authorizationCode_url, params=payload)
    os.startfile(r.url)


def getAccessToken(authCode):
    request_accessToken_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    payload = {'grant_type': 'authorization_code', 'code': authCode, 'redirect_uri': 'http://www.agxactly.com', 'client_id': consumer_key, 'client_secret': consumer_secret}
    r = requests.get(request_accessToken_url, params=payload)
    return r

def getId(accessToken):
    request_profile_url = 'https://api.linkedin.com/v2/me?projection=(id)'
    payload = {"Authorization": "Bearer "+accessToken }
    r = requests.get(request_profile_url, headers=payload)
    return r

def uploadMedia(id, accessToken, mediaBundle):
    upload_url = "https://api.linkedin.com/v2/assets?action=registerUpload"
    payload = {"Authorization": "Bearer "+accessToken }
    r = requests.post(upload_url, data=json.dumps(mediaBundle), headers=payload)
    return r

def reallyUploadMedia(id, accessToken, mediaUrl , upload_file):
    payload = {"Authorization": "Bearer "+accessToken }
    r = requests.post(mediaUrl, files = upload_file, headers=payload)
    return r
    
def Post(id, accessToken, postContents):
    post_url = 'https://api.linkedin.com/v2/ugcPosts'
    payload = {"Authorization": "Bearer "+accessToken }
    r = requests.post(post_url, data=json.dumps(postContents), headers=payload)
    return r    

#---- first, get an authorization code with this function
#authCodeBundle = getAuthCode()
    
# ---- then, copy-paste it here
#authCode = "AQT03Knu2zEtG9aLAF1mlsl2w7yYWKTYRZuc8GQNSj0AG3aZIq0aru78lBBgmqjxyQcqLCMHbgDQVJx4KKj9q64aEN9eQLNdL62QA4QfZq6o70ulGuGI01p0b8ncP59LqcmHzPZT-6pg4FK7R7TkokUZtuasHeGg03dFG2ZyPBEOO6r5p_NGoARmz9yaew"

# ------ use that authorization code to get an access token with the function below
#AccessTokenBundle = getAccessToken(authCode)
    
# ------ then, copy paste it here
accessToken = "AQW6hJSwMT-QgT1yWcw04O9lTceyehbR46sPDYm8Y4exhrqIUXrrFxlyTCLOZIxprHlDqXQT1-XH26j9pstDSq3gyYHf7FqtqXJrpaUB0L8byMRylVsmXHxfy8GR0Hqsy7hYdOwZpl40cgJ-Lvl0oOiqP6Y7aNbEv70Yel4MyUbUQ10FgZZC74x8ceH8jjeOztG_aCszx5_eBROzCLW6MmijDS5E3uIrzglDYwTRByjbO61Qpg01gk7hwj3zwjv3AMwidla11kwITNM0z1umkSCay3nQzhtuxVgqj_KMD_S0l0CWg2peQgs8RxkWitiDmqct2bMwwX3zxj_DB_4dVYA01Y-64w"

# ----- if you don't know your id, get it with the function below
#idBundle = getId(accessToken)

# ----- then, copy paste it here, and use it to get the posts!
id = 'J0t3aE87tl'

mediaBundle = {
    "registerUploadRequest": {
        "owner": "urn:li:person:J0t3aE87tl",
        "recipes": [
            "urn:li:digitalmediaRecipe:feedshare-image"
        ],
        "serviceRelationships": [
            {
                "identifier": "urn:li:userGeneratedContent",
                "relationshipType": "OWNER"
            }
        ]
    }
}
#uploadMediaBundle = uploadMedia(id, accessToken, mediaBundle)

mediaUrl = "https://api.linkedin.com/mediaUpload/C5622AQEiO6J3RZ8KFQ/feedshare-uploadedImage/0?ca=vector_feedshare&cn=uploads&m=AQJleTNmd9jHKwAAAXZKtNxJ2z3OqjlmEip1v917Ody9P617PVMKHTFlDA&app=88889106&sync=0&v=beta&ut=3CMa2PlmukQVw1"

pic = open("C:\\Users\\Gillies\\Desktop\\201015\\mk_only\\static\\img\\hey.png", "rb")
upload_file = {"Uploaded file": pic}
r = reallyUploadMedia(id, accessToken, mediaUrl, upload_file)


postContents = {
    "author": 'urn:li:person:J0t3aE87tl',
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "Test post here"
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}
#posts = Post(id, accessToken, postContents)

# ---- convert the reply to json
#postsJson = json.loads(posts.text)

# ---- print whichever part of the json bundle you'd like
#print(posts['message'])