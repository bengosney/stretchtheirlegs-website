module.exports = function (grunt) {
    const sass = require('sass');

    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        realFavicon: {
            favicons: {
            src: 'stl/static/fav-logo.svg',
            dest: 'stl/static/favicon/',
            options: {
                iconsPath: '/static/pages/favicon/',
                html: [ 'templates/favicon.html' ],
                design: {
                ios: {
                    pictureAspect: 'backgroundAndMargin',
                    backgroundColor: '#ffffff',
                    margin: '14%',
                    assets: {
                    ios6AndPriorIcons: false,
                    ios7AndLaterIcons: false,
                    precomposedIcons: false,
                    declareOnlyDefaultIcon: true
                    },
                    appName: 'Stretch Their Legs'
                },
                desktopBrowser: {},
                windows: {
                    pictureAspect: 'whiteSilhouette',
                    backgroundColor: '#582A72',
                    onConflict: 'override',
                    assets: {
                    windows80Ie10Tile: false,
                    windows10Ie11EdgeTiles: {
                        small: false,
                        medium: true,
                        big: false,
                        rectangle: false
                    }
                    },
                    appName: 'Stretch Their Legs'
                },
                androidChrome: {
                    pictureAspect: 'noChange',
                    themeColor: '#ffffff',
                    manifest: {
                    name: 'Stretch Their Legs',
                    display: 'standalone',
                    orientation: 'notSet',
                    onConflict: 'override',
                    declared: true
                    },
                    assets: {
                    legacyIcon: false,
                    lowResolutionIcons: false
                    }
                },
                safariPinnedTab: {
                    pictureAspect: 'silhouette',
                    themeColor: '#582A72'
                }
                },
                settings: {
                compression: 5,
                scalingAlgorithm: 'Mitchell',
                errorOnImageTooSmall: false,
                readmeFile: false,
                htmlCodeFile: false,
                usePathAsIs: false
                }
            }
            }
        },//*/
        postcss: {
            options: {
                map: true,
            },
            build: {
                processors: [
                    require('postcss-import')(),
                    require('postcss-import-url')(),
                    require('pixrem')(),
                    require('postcss-preset-env')({stage: 0}),
                    require('css-mqpacker')({sort: true}),
                    require('cssnano')({zindex: false})
                ]
            }
        },
        sass: {
            options: {
                implementation: sass,
                sourceMap: true
            },
            dist: {
                files: [{
                    expand: true,
                    cwd: 'scss',
                    src: ['*.scss'],
                    dest: 'stl/static/css',
                    ext: '.css'
                }]
            }
        },
        sass_globbing: {
            sass: {
                files: {
                    'scss/_imports.scss': [
                        'scss/*/**/*.scss',
                        '!scss/external/**/*.scss',
                        '!scss/mixins/**/*.scss'
                    ]
                },
                options: {
                    useSingleQuotes: true,
                }
            },
            external: {
                files: {
                    'scss/_external.scss': [
                        'scss/external/**/*.scss',
                    ]
                },
                options: {
                    useSingleQuotes: false,
                }
            },
            mixins: {
                files: {
                    'scss/_mixins.scss': [
                        'scss/mixins/**/*.scss',
                    ]
                },
                options: {
                    useSingleQuotes: false,
                }
            }
        },
        purifycss: {
            options: {
                minify: true,
                rejected: true,
                whitelist: []
            },
            target: {
                src: ['./**/templates/**/*.html', './pages/**/*.js'],
                css: ['stl/static/css/main.css'],
                dest: 'stl/static/css/main.css'
            }
        },
        webfont: {
            icons: {
                src: 'icons/build/**/*.svg',
                dest: 'stl/static/fonts',
                options: {
                    template: 'icons/template.css',
                    stylesheet: 'scss',
                    htmlDemo: false,
                    relativeFontPath: '/static/pages/fonts/',
                    destCss: 'scss/partials/',
                    customOutputs: [{
                        template: 'icons/json.template',
                        dest: 'icons/icons.json'
                    },
                        {
                            template: 'icons/python.template',
                            dest: 'icons/icons.py'
                        }]
                }
            }
        },
        jshint: {
            all: ['js/build/**/*.js']
        },
        babel: {
            options: {
                sourceMap: true,
                presets: ['@babel/preset-env']
            },
            dist: {
                expand: true,
                src: ['external/**/*.js', 'polyfill/**/*.js', 'local/**/*.js', 'compiled/**/*.js'],
                dest: 'js/build/',
                cwd: 'js'
            }
        },
        uglify: {
            options: {
                compress: {
                    drop_console: true
                },
                mangle: true
            },
            js: {
                files: {
                    'stl/static/js/script.js': 'js/build/**/*.js',
                    'pages/templates/pages/script.js': 'js/build/**/*.js'
                }
            }
        },
        browserSync: {
            dev: {
                bsFiles: {
                    src: [
                        'stl/static/**/*.css',
                        'stl/static/**/*.js',
                        'templates/**.html',
                        'pages/**/*.html',
                        './**/.html',
                    ]
                },
                options: {
                    watchTask: true,
                    proxy: "127.0.0.1:8000"
                }
            }
        },
        watch: {
            scss_compile: {
                files: ['scss/**/*.*'],
                tasks: ['scss'],
                options: {
                    spawn: false
                }
            },
            js: {
                files: ['js/local/**/*', 'js/external/**/*', 'js/polyfils/**/*', 'js/compiled/**/*'],
                tasks: ['js']
            },
            icons: {
                files: ['icons/build/**/*'],
                tasks: ['webfont']
            }
        }
    });

    grunt.registerTask('dev', ['browserSync', 'watch']);
    grunt.registerTask('icons', ['webfont']);
    grunt.registerTask('scss', ['sass_globbing', 'sass']);
    grunt.registerTask('js', ['babel', 'uglify']);
    grunt.registerTask('css', ['scss', 'purifycss', 'postcss']);
    grunt.registerTask('fav', ['realFavicon']);
    grunt.registerTask('compile', ['realFavicon', 'icons', 'css', 'js']);
    grunt.registerTask('default', ['compile']);
};
