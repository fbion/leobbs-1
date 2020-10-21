package model

import "gorm.io/gorm"

type Article struct {
	gorm.Model
	Aid uint
	Content string
	Images string
	PublishStatus uint;
}
