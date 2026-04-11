const config = {
  title: 'EchoSearch Articles',
  tagline: 'Search. Learn. Echo.',
  favicon: 'img/favicon.ico',

  url: 'https://echo-search.github.io',
  baseUrl: '/articles/',

  organizationName: 'echo-search',
  projectName: 'articles',

  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  presets: [
    [
      'classic',
      ({
        docs: {
          routeBasePath: '/', // docs become homepage
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/echo-search/articles/tree/main/',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig: ({
    navbar: {
      title: 'EchoSearch',
      items: [
        {
          to: '/',
          label: 'Articles',
          position: 'left',
        },
        {
          href: 'https://github.com/echo-search/articles',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [],
      copyright: `Copyright © ${new Date().getFullYear()} EchoSearch`,
    },
  }),
};

export default config;