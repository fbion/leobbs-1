package common

import (
	"database/sql"
	"gitee.com/leobbs/leobbs/app/orm_model"
	"github.com/gin-gonic/gin"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	_ "github.com/mattn/go-sqlite3"
	"github.com/naoina/toml"
	"github.com/ztrue/tracerr"
	"go.uber.org/zap"
	"html/template"
	"io/ioutil"
	"net/http"
	"os"
	"time"
)

var (
	DB *gorm.DB
	Config *AppConfig

	Logger, _ = zap.NewProduction()
	Sugar *zap.SugaredLogger
)

type ShowMessage interface {
	ShowMessage(c *gin.Context)
}
type msg struct {
	msg string
}
type umsg struct {
	msg string
	url string
}

type VBlogItem struct {
	aid            int
	content        sql.NullString
	publish_time   sql.NullString
	publish_status sql.NullInt64
}

/**
 * Logging error
 */
func LogError(err error) {
	Sugar.Error(tracerr.Sprint(tracerr.Wrap(err)))
}
/**
 * Logging info
 */
func LogInfo(msg string) {
	Sugar.Info(msg)
}
/**
 * close rows defer
 */
func CloseRowsDefer(rows *sql.Rows) {
	_ = rows.Close()
}
func (m *msg) ShowMessage(c *gin.Context) {
	c.HTML(http.StatusOK, "message.html", gin.H{
		"message": template.HTML(m.msg),
	})
}

func (m *umsg) ShowMessage(c *gin.Context) {
	c.HTML(http.StatusOK, "message.html", gin.H{
		"message": template.HTML(m.msg),
		"url":     m.url,
	})
}

func GetMinutes() string {
	return time.Now().Format("200601021504")
}

func GetDB(config *AppConfig) *gorm.DB {


	db, err := gorm.Open(sqlite.Open(config.Dbdsn), &gorm.Config{})

	if err != nil {
		LogError(err)
	}
	err = db.AutoMigrate(&orm_model.Article{})
	if err != nil {
		LogError(err)
	}
	err = db.AutoMigrate(&orm_model.Member{})
	if err != nil {
		LogError(err)
	}


	return db
}


func InitApp() {
	Config = GetConfig()
	DB = GetDB(Config)
	//异步刷新日志
	defer func() {
		err := Logger.Sync()
		if err != nil {
			LogError(err)
		}
	}()

	Sugar = Logger.Sugar()
}
type AppConfig struct {
	Dbdsn          string
	Admin_user       string
	Admin_password   string
	Site_name        string
	Site_description string
	ObjectStorage    struct {
		Aws_access_key_id     string
		Aws_secret_access_key string
		Aws_region            string
		Aws_bucket            string
		Cdn_url               string
	}
}

func GetConfig() *AppConfig {
	f, err := os.Open("./vol/config.toml")
	if err != nil {
		panic(err)
	}
	defer f.Close()
	buf, err := ioutil.ReadAll(f)
	if err != nil {
		panic(err)
	}
	var config AppConfig
	if err := toml.Unmarshal(buf, &config); err != nil {
		panic(err)
	}
	return &config
}
