import AminoLab
from io import BytesIO
from requests import get
client=AminoLab.Client()
def auth():
	client.auth(email=input("email»"),password=input("password»"))
def blocker_users():
	data=client.block_full_list()['blockerUidList']
	for userId in data:
		print(f"{client.get_user_info(userId=userId).nickname}»{userId}")
def blocked_users():
	data=client.block_full_list()['blockedUidList']
	for userId in data:
		print(f"{client.get_user_info(userId=userId).nickname}»{userId}")
def account_info():
    account_info = client.get_account_info()
    print(f"""Account info:
account created time >> {account_info['createdTime']}
email >> {account_info['email']}
phoneNumber >> {account_info['phoneNumber']}
nickname >> {account_info['nickname']}
user_Id >> {account_info['uid']}
amino_Id >> {account_info['aminoId']}""")
def comment_user():
	link_info = client.get_from_code(input("User Link >> "))
	message=input("message >>")
	while True:
		client.comment(comId=link_info.comId,userId=link_info.objectId,message=message)
def user_info():
    link_info = client.get_from_code(input("User Link >> "))
    user_info = client.get_user_info(userId=link_info.objectId)
    print(f"""User Info:
account created time >> {user_info.createdTime}
nickname >> {user_info.nickname}
content >> {user_info.content}
icon link >> {user_info.icon}
user_Id >> {link_info.objectId}
amino_Id >> {user_info.aminoId}""")
def comment_wiki():
	message=input("message >>")
	link_info = client.get_from_code(input("Wiki Link >> "))
	while True:
		client.comment(comId=link_info.comId,wikiId=link_info.objectId,message=message)
def comment_blog():
	message=input("message >>")
	link_info = client.get_from_code(input("Blog Link >> "))
	while True:
		client.comment(comId=link_info.comId,blogId=link_info.objectId,message=message)
def copy_profile():
	link_info = client.get_from_code(input("User Link >> "))
	comId, userId = link_info.comId, link_info.objectId
	user_info = client.get_user_info(userId=userId,comId=comId).json
	nickname = user_info["nickname"]
	description = user_info["content"]
	icon = BytesIO(get(user_info["icon"]).content)
	profile_style = user_info["extensions"]["style"]
	image_list = [BytesIO(get(str(user_info["mediaList"]).split("'")[1]).content)]
	if "backgroundColor" in profile_style:
		background_color = profile_style["backgroundColor"]
		client.edit_profile(backgroundColor=background_color,comId=comId)
	elif "backgroundMediaList" in profile_style:
		background_image = str(profile_style["backgroundMediaList"]).split("'")[1]
		client.edit_profile(backgroundImage=background_image,comId=comId)
	client.edit_profile(nickname=nickname,content=description,icon=icon,imageList=image_list,comId=comId)
def chat_info():
	link_info = client.get_from_code(input("Chat Link >> "))
	ndc_Id = link_info.comId; thread_Id = link_info.objectId
	chat_info = client.get_chat_thread(comId=ndc_Id, chatId=thread_Id)
	print(f"""Chat info:
title >> {chat_info['title']}
content >> {chat_info['content']}
members_count >> {chat_info['membersCount']}
tippers_count >> {chat_info['tipInfo']['tippersCount']}
tipped_coins >> {chat_info['tipInfo']['tippedCoins']}
thread_Id >> {thread_Id}""")
def copy_chat():
	link_info = client.get_from_code(input("Chat Link >> "))
def my_community():
	clients = client.sub_clients()
	for x, name in enumerate(clients.name, 1):
		print(f"{x}.{name}")
	return clients.comId[int(input("Select the community >> ")) - 1]
def my_chats(comId:str=None):
	chats = client.get_chat_threads(size=100,comId=comId)
	for x, title in enumerate(clients.title, 1):
		print(f"{x}.{name}")
	return chats.chatId[int(input("Select the chat >>"))-1]
def raid_chat():
	message=input("message >>")
	messageType=input("type >>")
	print("1-global raid 2-local raid")
	select=int(input("select >>"))
	if select==1:
		chatId=my_chats()
		while True:
			client.send_message(chatId=chatId,message=message,messageType=messageType)
	else:
		comId=my_community()
		chatId=my_chats(comId)
		while True:
			client.send_message(comId=comId,chatId=chatId,message=message,messageType=messageType)
def spam_post():
	title=input("title >>")
	content=input("content >>")
	comId=my_community()
	while True:
		client.post_blog(comId=comId,title=title,content=content)
def spam_wiki():
	title=input("title >>")
	content=input("content >>")
	comId=my_community()
	while True:
		client.post_wiki(comId=comId,title=title,content=content)
def community_info():
	com_info=client.get_community_info(comId=client.get_from_code(input("Community Link >>")).comId)
	print(f"""name >> {com_info['name']}
	amino_Id >> {com_info['endpoint']}
	updated Time >> {com_info['updatedTime']}
	created Time >> {com_info['createdTime']}
	icon link >> {com_info['icon']}
	keywords >> {com_info['keywords']}
	content >> {com_info['content']}""")
def check_in_all():
	comIds= client.sub_clients().comId
	for comId in comIds:
		client.check_in(comId=comId)
def edit_profile():
	client.edit_profile(content=input("content >>"),nickname=input("nickname >>"))
def edit_local_profile():
	client.edit_profile(content=input("content >>"),nickname=input("nickname >>"),comId=my_community())
def edit_all_local_profile():
	nickname=input("nickname >>")
	content=input("content >>")
	comIds= client.sub_clients().comId
	for comId in comIds:
		client.edit_profile(content=content,nickname=nickname,comId=comId)
def join_local_chat():
	comId=my_community()
	chatsId=get_public_chat_threads(size=0,start=100,comId=comId).chatId
	for chatId in chatsId:
		client.join_chat(comId=comId,chatId=chatId)
def follow_user():
	print("1-global,2-local")
	select=int(input("select >>"))
	if select==1:
		start=int(-100)
		while True:
			start+= 100
			userId=client.get_all_users(type="online",size=100,start=start).userId
			if userId==[]:exit()
			else:client.follow(userId=userId)
	else:
		comId=my_community()
		start=int(-100)
		while True:
			start+= 100
			userId=client.get_all_users(type="recent",size=100,start=start,comId=comId).userId
			if userId==[]:exit()
			else:client.follow(userId=userId,comId=comId)
def unfillow_user():
	print("1-global,2-local")
	select=int(input("select >>"))
	if select==1:
		start=int(-100)
		while True:
			start+= 100
			usersId=get_user_following(userId=client.userId,size=100,start=start).userId
			if usersId==[]:exit()
			else:
				for userId in usersId:
					client.unfollow(userId=userId)
	else:
		comId=my_community()
		start=int(-100)
		while True:
			start+= 100
			usersId=get_user_following(userId=client.userId,size=100,start=0,comId=comId).userId
			if usersId==[]:exit()
			else:
				for userId in usersId:
					client.unfollow(userId=userId,comId=comId)
def leave_chats():
	print("1-global,2-local")
	select=int(input("select >>"))
	if select==1:
		while True:
			chatsId=client.get_chat_threads(size=100).chatId
			if chatsId==[]:exit()
			else:client.leave_chat()
	else:
		comId=my_community()
		while True:
			chatsId=client.get_chat_threads(comId=comId,size=100).chatId
			if chatsId==[]:exit()
			else:client.leave_chat(comId=comId,chatsId=chatsId)
def leave_community():
	comIds= client.sub_clients().comId
	for comId in comIds:
		client.leave_community(comId=comId)
def kik_in_community():
	comId=my_community()
	chatId=my_chats(comId=comId)
	while True:
		users_count=client.get_chat_thread(chatId=chatId)["membersCount"]
		if users_count > 100:
			chat_users=client.get_chat_users(comId=comId,chatId=chatId,start=0,size=100).userId
			for userId in chat_users:
				if userId != client.userId:client.kik(comId=comId,chatId=chatId,userId=userId)
				else:pass
		else:
			chat_users=client.get_chat_users(comId=comId,chatId=chatId,start=0,size=100).userId
			for userId in chat_users:
				if userId !=client.userId:client.kik(comId=comId,chatId=chatId,userId=userId)
				else:pass
def kik_in_global():
	chatId=chats()
	while True:
		users_count=client.get_chat_thread(chatId=chatId)["membersCount"]
		if users_count > 100:
			chat_users=client.get_chat_users(chatId=chatId,start=0,size=100).userId
			for userId in chat_users:
				if userId != client.userId:client.kik(chatId=chatId,userId=userId)
				else:pass
		else:
			chat_users=client.get_chat_users(chatId=chatId,start=0,size=100).userId
			for userId in chat_users:
				if userId !=client.userId:client.kik(chatId=chatId,userId=userId)
				else:pass
def kik_all_in_chats():
	print("1-global 2-local")
	select=int(input("Select>>"))
	if select==1: kik_in_community()
	else: kik_in_global()
def copy_wiki():
		link_info=client.get_from_code(input("Blog link:- "))
		wikiId=link_info.objectId
		comId=link_info.comId
		blog_info = client.get_blog_info(wikiId=wikiId,comId=comId)
		blog_style = blog_info["extensions"]["style"]
		captions_and_images = str(blog_info["mediaList"]).split()
		image_list = []
		caption_list = []
		for caption in captions_and_images:
			if "']" in caption:
				caption_list.append(caption.strip("'],"))
		for image in captions_and_images:
			if "http" in image:
				image_list.append(BytesIO(get(image.strip("',")).content))
		if "backgroundColor" in blog_style:
			client.post_wiki(
				title=blog_info["title"],
				content=blog_info["content"],
				imageList=image_list,
				captionList=caption_list,
				backgroundColor=blog_style["backgroundColor"],comId=comId)
		elif "backgroundMediaList" in blog_style:
			background_image = [
				[100, str(blog_style["backgroundMediaList"]).split("'")[1], None]]
			client.post_wiki(comId=comId,
				title=blog_info["title"],
				content=blog_info["content"],
				imageList=image_list,
				captionList=caption_list,
				extensions={
					"style": {
						"backgroundMediaList": background_image}})
def copy_blog():
	link_info=client.get_from_code(input("Blog link:- "))
	blogId=link_info.objectId
	comId=link_info.comId
	blog_info = client.get_blog_info(blogId=blogId,comId=comId)
	blog_style = blog_info["extensions"]["style"]
	captions_and_images = str(blog_info["mediaList"]).split()
	image_list = []
	caption_list = []
	for caption in captions_and_images:
			if "']" in caption:
				caption_list.append(caption.strip("'],"))
	for image in captions_and_images:
			if "http" in image:
				image_list.append(BytesIO(get(image.strip("',")).content))
			if "backgroundColor" in blog_style:
				client.post_blog(
				title=blog_info["title"],
				content=blog_info["content"],
				imageList=image_list,
				captionList=caption_list,
				backgroundColor=blog_style["backgroundColor"],comId=comId)
			elif "backgroundMediaList" in blog_style:
				background_image = [
				[100, str(blog_style["backgroundMediaList"]).split("'")[1], None]]
			client.post_blog(comId=comId,
				title=blog_info["title"],
				content=blog_info["content"],
				imageList=image_list,
				captionList=caption_list,
				extensions={
					"style": {
"backgroundMediaList": background_image}})
def copy_chat():
	link_data=client.get_from_code(input("Chat link >>> "))
	comId=link_data.comId
	chat_info =client.get_chat_thread(chatId=link_data.objectId,comId=comId)
	chat_style = chat_info["extensions"]
	client.edit_chat(chatId=my_chats(comId=comId),comId=comId,title = chat_info["title"],content = chat_info["content"],icon = chat_info["icon"],keywords = chat_info["keywords"],fansOnly=chat_style["fansOnly"],backgroundImage = chat_style["bm"][1])
def clear_wiki_profile():
	comId=my_community()
	while True:
		blogs_count = client.get_user_info(userId=client.userId).json["itemsCount"]
		if blogs_count > 0:
					created_wikis =client.get_user_wikis(userId=client.userId, start=0, size=100,comId=comId).wikiId
					for wiki_id in created_wikis:
						client.delete_wiki(wikiId=wiki_id,comId=comId)
		elif blogs_count == 0:print("Deleted all blogs!")
def clear_post_profile():
	comId=my_community()
	while True:
		blogs_count = client.get_user_info(userId=client.userId).json["blogsCount"]
		if blogs_count > 0:
					created_blogs =client.get_user_blogs(userId=client.userId, start=0, size=100,comId=comId).blogId
					for blog_id in created_blogs:
						client.delete_blog(blogId=blog_id,comId=comId)
		elif blogs_count == 0:print("Deleted all blogs!")
def follow_spam():
	link_info=client.get_from_code(input("User link>>"))
	while True:
		client.follow(userId=link_info.objectId,comId=link_info.comId);client.unfollow(userId=link_info.objectId,comId=link_info.comId)
def join_leave_spam():
	print("1-global,2-local")
	select=int(input("select >>"))
	if select==1:
		chatId=my_chats()
		while True:
			client.join_chat(chatId=chatId);client.leave_chat(chatId=chatId)
	else:
		comId=my_community
		chatId=my_chats(comId=comId)
		while True:
			client.join_chat(chatId=chatId,comId=comId);client.leave_chat(chatId=chatId,comId=comId)
def ban_nickname():
	com_Id=my_community()
	target=input("nickname for ban >>")
	while True:
		users=client.get_all_users(type="recent",comId=com_Id,start=0,size=100)
		for nickname , id in zip(users.nickname, users.userId):
			if target in nickname:
				print(nickname)
				client.ban(comId=com_Id,userId=id,reason="хохол ебаный пидор")
			else:pass
		if users==[]:exit()
def unban_nickname():
	com_Id=my_community()
	target=input("nickname for unban >>")
	start=int(-100)
	while True:
			start+= 100
			users=client.get_all_users(type="banned",comId=com_Id,start=start,size=100)
			for nickname , id in zip(users.nickname, users.userId):
				if target in nickname:
					print(nickname)
					client.unban(comId=com_Id,userId=id,reason="норм чел русский")
			else:pass
def ban_all():
	com_Id=my_community()
	start=int(-100)
	while True:
		start+= 100
		usersId=client.get_all_users(type="recent",comId=com_Id,start=start,size=100).userId
		if usersId==[]:exit()
		else:
			for id in usersId:
				client.ban(comId=com_Id,userId=id,reason="хохол пидор ебаный")
def unban_all():
	com_Id=my_community()
	start=int(-100)
	while True:
			start+= 100
			usersId=client.get_all_users(type="banned",comId=com_Id,start=0,size=100).userId
			if usersId==[]:exit()
			else:
				for id in usersId:
					client.unban(comId=com_Id,userId=id,reason="норм чел русский")
def clear_comments_profile():
	print("1 global 2 local")
	select=int(input("select >>"))
	if select==1:
		while True:
			comments=client.get_wall_comments(userId=client.userId,size=100,sorting="newest").commentId
			for comment in comments:
				client.delete_comment(commentId=comment,userId=client.userId)
			if comments==[]:exit()
	else:
		com_Id=my_community()
		while True:
			comments=client.get_wall_comments(userId=client.userId,size=100,sorting="newest",comId=com_Id).commentId
			for comment in comments:
				client.delete_comment(commentId=comment,userId=client.userId,comId=com_Id)
			if comments==[]:exit()
def report_user():
	reason=input("reason>>")
	link_data=client.get_from_code(input("link user>>"))
	while True:
		client.report(comId=link_data.comId,userId=link_data.objectId,flag_Type=2,reason=reason)
def report_chat():
	reason=input("reason>>")
	link_data=client.get_from_code(input("link chat>>"))
	while True:
		client.report(comId=link_data.comId,chatId=link_data.objectId,flag_Type=2,reason=reason)
def report_blog():
	reason=input("reason>>")
	link_data=client.get_from_code(input("link blog>>"))
	while True:
		client.report(comId=link_data.comId,blogId=link_data.objectId,flag_Type=2,reason=reason)
def report_wiki():
	reason=input("reason>>")
	link_data=client.get_from_code(input("link wiki>>"))
	while True:
		client.report(comId=link_data.comId,wikiId=link_data.objectId,flag_Type=2,reason=reason)
def report_community():
	reason=input("reason>>")
	link_data=client.get_from_code(input("link community>>"))
	while True:
		client.report(comId=link_data.comId,flag_Type=2,reason=reason)
def delete_chat():
	print("1-global,2-local")
	select=int(input("select>>"))
	if select==1:
		com_Id=my_community()
		chatId=my_chats(comId=comId)
		client.delete_chat(comId=com_Id,chatId=chatId)
	else:
		chatId=my_chats(comId=comId)
		client.delete_chat(comId=com_Id,chatId=chatId)
def bubble():
	print("1-global,2-local")
	select=int(input("select >>"))
	file=get(input("link bubble image >>")).content
	if select==1:
		client.upload_bubble(bubbleId=client.generate_bubble(file=file))
	else:
		com_Id=my_community()
		client.upload_bubble(bubbleId=client.generate_bubble(comId=com_Id,file=file),comId=com_Id)
def report_utilz():
	print("""1-report user
2-report community
3-report chat
4-report wiki
5-report blog""")
	select=int(input("select >>"))
	if  select==1:report_user()
	if  select==2:report_community()
	if  select==3:report_chat()
	if  select==4:report_wiki()
	if  select==5:report_blog()
def profile_utilz():
	print("""1-edit global profile
2-edit profile in community
3-edit profile all community
4-applay bubble
5-clear comment profile
6-follow users
7-unfollow user followers""")
	select=int(input("select >>"))
	if  select==1:edit_profile()
	if  select==2:edit_local_profile()
	if  select==3:edit_all_local_profile()
	if  select==4:bubble()
	if select==5:clear_comments_profile()
	if  select==6:follow_user()
	if select==7:unfollow_user()
def spam_utilz():
	print("""1-spam comment user
2-spam comment wiki
3-spam comment post
4-spam wiki
5-spam blog
6-chat raid
7-join leave spam
8-follow unfolow spam""")
	select=int(input("select >>"))
	if  select==1:comment_user()
	if  select==2:comment_wiki()
	if  select==3:comment_blog()
	if  select==4:spam_wiki()
	if  select==5:spam_post()
	if select==6:raid_chat()
	if select==7:join_leave_spam()
	if select==8:follow_spam()
def info_utilz():
	print("""1-get blocker user
2-get blocked users
3-account info
4-user info
5-chat info
6-community info""")
	select=int(input("select >>"))
	if select==1:blocker_users()
	if select==2:blocked_users()
	if select==3:account_info()
	if select==4:user_info()
	if select==5:chat_info()
	if select==6:community_info()
def copy_utilz():
	print("""1-copy_wiki
2-copy blog
3-copy chat
4-report wiki
5-report blog""")
	select=int(input("select >>"))
	if  select==1:copy_wiki()
	if  select==2:copy_blog()
	if  select==3:copy_chat()
	if  select==4:report_wiki()
	if  select==5:report_blog()
def moderation_utilz():
	print("""1-kik all users chat
2-ban nickname
3-unban nickname
4-ban all
5-unban all""")
	select=int(input("select >>"))
	if  select==1:kik_all_in_chats()
	if  select==2:ban_nickname()
	if  select==3:unban_nickname()
	if  select==4:ban_all()
	if  select==5:unban_all()
def other_utilz():
	print("""1-chek in all community
2-leave chats
3-leave all community
4-clear profile wikis
5-clear profile blogs
6-delete chat""")
	select=int(input("select >>"))
	if  select==1:check_in_all()
	if  select==2:leave_chats()
	if  select==3:leave_community()
	if  select==4:clear_wiki_profile()
	if  select==5:clear_post_profile()
	if  select==6:delete_chat()
def main():
	try:
		auth()
		print("""1-spam utilz
2-report utilz
3-info utilz
4-other utilz
5-profile utilz
6-copy utilz
7-moderation utilz""")
		select=int(input("select >>"))
		if select==1:spam_utilz()
		if select==2:report_utilz()
		if select==3:info_utilz()
		if select==4:other_utilz()
		if select==5:profile_utilz()
		if select==6:copy_utilz()
		if select==7:moderation_utilz()
	except Exception as e:
		print(e)
main()