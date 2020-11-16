package forum_service

import (
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/pkg/common"
)

func GetForumList() (forumList []*orm_model.Forum, err error) {
	result := common.DB.Find(&forumList)
	if result.Error == nil {
		return forumList, nil
	} else {
		return nil, result.Error
	}
}

func GetForum(id int64) (forum *orm_model.Forum, err error) {
	result := common.DB.First(&forum, id)
	if result.Error == nil {
		return forum, nil
	} else {
		return nil, result.Error
	}
}