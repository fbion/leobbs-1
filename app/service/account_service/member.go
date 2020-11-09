package account_service

import (
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/pkg/common"
)

func RegisterNewMember(mo orm_model.Member) (id int64){
	result := common.DB.Create(mo)
	if result.Error != nil {
		common.Sugar.Infof(" register new member error: %v", result.Error)
	}
	return mo.ID
}