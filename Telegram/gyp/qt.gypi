# This file is part of Telegram Desktop,
# the official desktop version of Telegram messaging app, see https://telegram.org
#
# Telegram Desktop is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# It is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# In addition, as a special exception, the copyright holders give permission
# to link the code of portions of this program with the OpenSSL library.
#
# Full license: https://github.com/telegramdesktop/tdesktop/blob/master/LICENSE
# Copyright (c) 2014 John Preston, https://desktop.telegram.org

{
  'variables': {
    'variables': {
      'variables': {
        'variables': {
          'variables': {
            'conditions': [
              [ 'build_macold', {
                'qt_version%': '5.3.2',
              }, {
                'qt_version%': '<!(echo /usr/include/<(triplet)/qt5/QtCore/*/ | grep -Po "\d+\.\d+\.\d+")',
              }]
            ],
          },
          'qt_libs': [
            'Qt5PlatformSupport',
            'Qt5Network',
            'Qt5Widgets',
            'Qt5Gui',
          ],
          'qt_version%': '<(qt_version)',
          'linux_path_qt%': '/usr/lib/<(triplet)/qt5',
        },
        'qt_version%': '<(qt_version)',
        'qt_loc_unix': '<(linux_path_qt)',
        'conditions': [
          [ 'build_win', {
            'qt_lib_prefix': '<(ld_lib_prefix)',
            'qt_lib_debug_postfix': 'd<(ld_lib_postfix)',
            'qt_lib_release_postfix': '<(ld_lib_postfix)',
            'qt_libs': [
              '<@(qt_libs)',
              'Qt5Core',
              'qtmain',
              'qwindows',
              'qtfreetype',
              'qtpcre',
            ],
          }],
          [ 'build_mac', {
            'qt_lib_prefix': '<(ld_lib_prefix)',
            'qt_lib_debug_postfix': '_debug<(ld_lib_postfix)',
            'qt_lib_release_postfix': '<(ld_lib_postfix)',
            'qt_libs': [
              '<@(qt_libs)',
              'Qt5Core',
              'qgenericbearer',
              'qcocoa',
            ],
          }],
          [ 'build_mac and not build_macold', {
            'qt_libs': [
              '<@(qt_libs)',
              'Qt5Core',
              'qtfreetype',
              'qtpcre',
            ],
          }],
          [ 'build_linux', {
            'qt_lib_prefix': '',
            'qt_lib_debug_postfix': '',
            'qt_lib_release_postfix': '',
            'qt_libs': [
              '<@(qt_libs)',
              'Qt5Core',
            ],
          }],
        ],
      },
      'qt_version%': '<(qt_version)',
      'qt_loc_unix': '<(qt_loc_unix)',
      'qt_version_loc': '<!(python -c "print(\'<(qt_version)\'.replace(\'.\', \'_\'))")',
      'qt_libs_debug': [
        '<!@(python -c "for s in \'<@(qt_libs)\'.split(\' \'): print(\'<(qt_lib_prefix)\' + s + \'<(qt_lib_debug_postfix)\')")',
      ],
      'qt_libs_release': [
        '<!@(python -c "for s in \'<@(qt_libs)\'.split(\' \'): print(\'<(qt_lib_prefix)\' + s + \'<(qt_lib_release_postfix)\')")',
      ],
    },
    'qt_libs_debug': [ '<@(qt_libs_debug)' ],
    'qt_libs_release': [ '<@(qt_libs_release)' ],
    'qt_version%': '<(qt_version)',
    'conditions': [
      [ 'build_win', {
        'qt_loc': '../../../Libraries/qt<(qt_version_loc)/qtbase',
      }, {
        'qt_loc': '<(qt_loc_unix)',
      }],
    ],
  },

  'configurations': {
    'Debug': {
      'conditions' : [
        [ 'build_win', {
          'msvs_settings': {
            'VCLinkerTool': {
              'AdditionalDependencies': [
                '<@(qt_libs_debug)',
              ],
            },
          },
        }],
        [ 'build_mac', {
          'xcode_settings': {
            'OTHER_LDFLAGS': [
              '<@(qt_libs_debug)',
              '/usr/local/lib/libz.a',
            ],
          },
        }],
      ],
    },
    'Release': {
      'conditions' : [
        [ 'build_win', {
          'msvs_settings': {
            'VCLinkerTool': {
              'AdditionalDependencies': [
                '<@(qt_libs_release)',
              ],
            },
          },
        }],
        [ 'build_mac', {
          'xcode_settings': {
            'OTHER_LDFLAGS': [
              '<@(qt_libs_release)',
              '/usr/local/lib/libz.a',
            ],
          },
        }],
      ],
    },
  },

  'include_dirs': [
    '/usr/include/<(triplet)/qt5',
    '/usr/include/<(triplet)/qt5/QtCore',
    '/usr/include/<(triplet)/qt5/QtGui',
    '/usr/include/<(triplet)/qt5/QtCore/<(qt_version)/',
    '/usr/include/<(triplet)/qt5/QtGui/<(qt_version)/',
    '/usr/include/<(triplet)/qt5/QtCore/<(qt_version)/QtCore',
    '/usr/include/<(triplet)/qt5/QtGui/<(qt_version)/QtGui',
  ],
  'library_dirs': [
    '<(qt_loc)/lib',
    '<(qt_loc)/plugins',
    '<(qt_loc)/plugins/bearer',
    '<(qt_loc)/plugins/platforms',
    '<(qt_loc)/plugins/imageformats',
  ],
  'defines': [
    'QT_WIDGETS_LIB',
    'QT_NETWORK_LIB',
    'QT_GUI_LIB',
    'QT_CORE_LIB',
  ],
  'conditions': [
    [ 'build_linux', {
      'library_dirs': [
        '<(qt_loc)/plugins/platforminputcontexts',
      ],
      'libraries': [
        '<@(qt_libs_release)',
        'crypto',
        'X11',
        'glib-2.0',
        'pthread',
      ],
      'include_dirs': [
        '<(qt_loc)/mkspecs/linux-g++',
      ],
      'ldflags': [
        '-pthread',
        '-g',
        '-rdynamic',
      ],
    }],
    [ 'build_mac', {
      'xcode_settings': {
        'OTHER_LDFLAGS': [
          '-lcups',
        ],
      },
    }],
  ],

  'rules': [{
    'rule_name': 'qt_moc',
    'extension': 'h',
    'outputs': [
      '<(SHARED_INTERMEDIATE_DIR)/<(_target_name)/moc/moc_<(RULE_INPUT_ROOT).cpp',
    ],
    'action': [
      '<(qt_loc)/bin/moc<(exe_ext)',

      # Silence "Note: No relevant classes found. No output generated."
      '--no-notes',

      '<!@(echo $CPPFLAGS | grep -Po "[-]([IDU]\s*\S*|E)")',
      '<!@(python -c "for s in \'<@(_defines)\'.split(\' \'): print(\'-D\' + s)")',
      # '<!@(python -c "for s in \'<@(_include_dirs)\'.split(\' \'): print(\'-I\' + s)")',
      '<(RULE_INPUT_PATH)',
      '-o', '<(SHARED_INTERMEDIATE_DIR)/<(_target_name)/moc/moc_<(RULE_INPUT_ROOT).cpp',
    ],
    'message': 'Moc-ing <(RULE_INPUT_ROOT).h..',
    'process_outputs_as_sources': 1,
  }],
}
