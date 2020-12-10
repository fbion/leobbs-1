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
	//PostId 是对应的帖子的帖子id，主题也是一个帖子
	PostId int64;
}
