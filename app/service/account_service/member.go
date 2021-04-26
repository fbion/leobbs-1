package account_service

import (
	"github.com/leobbs/leobbs/app/orm_model"
	"github.com/leobbs/leobbs/app/vo"
	"github.com/leobbs/leobbs/pkg/common"
)

func RegisterNewMember(mo orm_model.Member) (id int64) {
	result := common.DB.Create(mo)
	if result.Error != nil {
		common.Sugar.Infof(" register new member error: %v", result.Error)
	}
	return mo.ID
}

func CountRegMember() (cnt int64) {
	common.DB.Model(&orm_model.Member{}).Count(&cnt)
	return cnt
}

func GetUserInfo(uid int64) vo.UserInfoVo {
	var sourceUserInfo orm_model.Member
	var outUserInfo vo.UserInfoVo
	common.DB.Find(&sourceUserInfo, uid)
	if sourceUserInfo.ID > 0 {
		outUserInfo.Uid = sourceUserInfo.ID
		outUserInfo.NickName = sourceUserInfo.Username
		outUserInfo.UserName = sourceUserInfo.Username
	}
	return outUserInfo
}
