package orm_model

import (
	"gorm.io/gorm"
	"time"
)

type Article struct {
	ID        int64 `gorm:"primarykey"`
	CreatedAt time.Time
	UpdatedAt time.Time
	DeletedAt gorm.DeletedAt `gorm:"index"`
	Content string
	Images string
	PublishStatus int;
}
