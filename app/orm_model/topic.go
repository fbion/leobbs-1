package orm_model

import (
	"gorm.io/gorm"
	"time"
)

type Topic struct {

	ID        int64 `gorm:"primarykey"`
	CreatedAt time.Time
	UpdatedAt time.Time
	DeletedAt gorm.DeletedAt `gorm:"index"`
	Title string
	AuthorUid int64
	PublishStatus int;
	//TopicId 为0表示主贴，否则就是回复
	TopicId int64;
	ForumId int64;
}
