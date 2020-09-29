module.exports = {
  title: '雷傲论坛LeoBBS',
  tagline: '雷傲论坛浴火重生',
  url: 'https://gitee.com/leobbs',
  baseUrl: '/',
  onBrokenLinks: 'throw',
  favicon: 'img/favicon.ico',
  organizationName: 'leobbs', // Usually your GitHub org/user name.
  projectName: 'leobbs', // Usually your repo name.
  themeConfig: {
    navbar: {
      title: 'LeoBBS',
      logo: {
        alt: 'My Site Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          to: 'docs/',
          activeBasePath: 'docs',
          label: '文档',
          position: 'left',
        },
        {
          href: 'https://gitee.com/leobbs/leobbs',
          label: '源代码',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: '文档',
          items: [
            {
              label: 'Style Guide',
              to: 'docs/',
            },
            {
              label: 'Second Doc',
              to: 'docs/doc2/',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Gitee',
              href: 'https://gitee.com/leobbs',
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Gitee',
              href: 'https://gitee.com/leobbs',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Leobbs team.`,
    },
  },
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          editUrl:
            'https://github.com/facebook/docusaurus/edit/master/website/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
};
