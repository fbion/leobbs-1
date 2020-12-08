package form

type NewPostForm struct {
	Fid int64 `form:"fid" binding:"required"`
	Tid int64 `form:"tid" binding:"required"`
	Content string `form:"inpost" binding:"required"`
}
