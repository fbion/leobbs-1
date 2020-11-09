package orm_model

import (
	"gorm.io/gorm"
	"time"
)

type Member struct {
	ID        int64 `gorm:"primarykey"`
	CreatedAt time.Time
	UpdatedAt time.Time
	DeletedAt gorm.DeletedAt `gorm:"index"`
	Username string
	Password string
	Email string
	Salt string;
	IsDeleted bool
	IsLocked bool
}
