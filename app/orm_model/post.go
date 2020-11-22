package orm_model

import (
	"gorm.io/gorm"
	"time"
)

type Post struct {
	ID        int64 `gorm:"primarykey"`
	CreatedAt time.Time
	UpdatedAt time.Time
	DeletedAt gorm.DeletedAt `gorm:"index"`
	Content string
	TopicId int64
	PostUid int64
	PublishStatus int;
}
