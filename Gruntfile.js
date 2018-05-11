module.exports = function (grunt) {
    'use strict';
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        // we could just concatenate everything, really
        // but we like to have it the complex way.
        // also, in this way we do not have to worry
        // about putting files in the correct order
        // (the dependency tree is walked by r.js)
        less: {
            dist: {
                options: {
                    paths: [],
                    strictMath: false,
                    sourceMap: true,
                    outputSourceFiles: true,
                    sourceMapURL: '++theme++custom/styles/common-compiled.css.map',
                    sourceMapFilename: 'src/troupedu8/common/theme/styles/common-compiled.css.map',
                    modifyVars: {
                        "isPlone": "false"
                    }
                },
                files: {
                    'src/troupedu8/common/theme/styles/common-compiled.css': 'src/troupedu8/common/theme/less/common-compiled.local.less'
                }
            }
        },

        watch: {
            scripts: {
                files: ['src/troupedu8/common/theme/less/*.less'],
                tasks: ['less']
            }
        },
    });

    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.registerTask('default', ['watch']);
};
