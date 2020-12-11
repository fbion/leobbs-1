package form

type EditTopicForm struct {
	Tid int64 `form:"tid" binding:"required"`
	Fid int64 `form:"fid" binding:"required"`
	Title string `form:"intopictitle" binding:"required"`
	Content string `form:"inpost" binding:"required"`
}
