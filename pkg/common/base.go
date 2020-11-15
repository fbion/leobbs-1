package common

import (
	"database/sql"
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/app/skins"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"

	_ "github.com/mattn/go-sqlite3"
	"github.com/naoina/toml"
	"github.com/ztrue/tracerr"
	"go.uber.org/zap"
	"io/ioutil"
	"os"
	"time"
)

var (
	DB *gorm.DB
	Config *AppConfig

	Logger, _ = zap.NewProduction()
	Sugar *zap.SugaredLogger
)

type Msg struct {
	Msg string
}
type Umsg struct {
	Msg string
	Url string
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
func ShowMessage(c *gin.Context, m *Msg) {



	pongoContext := pongo2.Context{
		"message":         m.Msg,
		"imagesurl": "/assets",
		"skin":      "leobbs",
		"hello":     "world",
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}

	c.HTML(200, "message.html",
		pongoContext)
	return
}


func ShowUMessage(c *gin.Context, m *Umsg) {

	pongoContext := pongo2.Context{
		"imagesurl": "/assets",
		"skin":      "leobbs",
		"message":         m.Msg,
		"url":             m.Url,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}

	c.HTML(200, "message.html",
		pongoContext)
	return
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
	Admin_user       []string
	Site_name        string
	Site_description string
	Key_of_encrypt string
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
