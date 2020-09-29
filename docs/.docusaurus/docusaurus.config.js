export default {
  "title": "雷傲论坛LeoBBS",
  "tagline": "雷傲论坛浴火重生",
  "url": "https://gitee.com/leobbs",
  "baseUrl": "/",
  "onBrokenLinks": "throw",
  "favicon": "img/favicon.ico",
  "organizationName": "leobbs",
  "projectName": "leobbs",
  "themeConfig": {
    "navbar": {
      "title": "LeoBBS",
      "logo": {
        "alt": "My Site Logo",
        "src": "img/logo.svg"
      },
      "items": [
        {
          "to": "docs/",
          "activeBasePath": "docs",
          "label": "文档",
          "position": "left"
        },
        {
          "href": "https://gitee.com/leobbs/leobbs",
          "label": "源代码",
          "position": "right"
        }
      ],
      "hideOnScroll": false
    },
    "footer": {
      "style": "dark",
      "links": [
        {
          "title": "文档",
          "items": [
            {
              "label": "Style Guide",
              "to": "docs/"
            },
            {
              "label": "Second Doc",
              "to": "docs/doc2/"
            }
          ]
        },
        {
          "title": "Community",
          "items": [
            {
              "label": "Gitee",
              "href": "https://gitee.com/leobbs"
            }
          ]
        },
        {
          "title": "More",
          "items": [
            {
              "label": "Gitee",
              "href": "https://gitee.com/leobbs"
            }
          ]
        }
      ],
      "copyright": "Copyright © 2020 Leobbs team."
    },
    "colorMode": {
      "defaultMode": "light",
      "disableSwitch": false,
      "respectPrefersColorScheme": false,
      "switchConfig": {
        "darkIcon": "🌜",
        "darkIconStyle": {},
        "lightIcon": "🌞",
        "lightIconStyle": {}
      }
    }
  },
  "presets": [
    [
      "@docusaurus/preset-classic",
      {
        "docs": {
          "sidebarPath": "C:\\workspace\\leobbs\\leobbs\\docs\\sidebars.js",
          "editUrl": "https://github.com/facebook/docusaurus/edit/master/website/"
        },
        "theme": {
          "customCss": "C:\\workspace\\leobbs\\leobbs\\docs\\src\\css\\custom.css"
        }
      }
    ]
  ],
  "onDuplicateRoutes": "warn",
  "customFields": {},
  "plugins": [],
  "themes": []
};