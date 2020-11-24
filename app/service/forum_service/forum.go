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

func GetForum(id int64) (*orm_model.Forum, error) {
	var tmpForum orm_model.Forum
	common.Sugar.Infof("forum query with id: %d", id)
	result := common.DB.First(&tmpForum, id)
	common.Sugar.Infof("GetForum: %v", tmpForum)
	if result.Error == nil {
		return &tmpForum, nil
	} else {
		return nil, result.Error
	}
}