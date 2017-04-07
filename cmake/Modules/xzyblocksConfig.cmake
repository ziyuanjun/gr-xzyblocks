INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_XZYBLOCKS xzyblocks)

FIND_PATH(
    XZYBLOCKS_INCLUDE_DIRS
    NAMES xzyblocks/api.h
    HINTS $ENV{XZYBLOCKS_DIR}/include
        ${PC_XZYBLOCKS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    XZYBLOCKS_LIBRARIES
    NAMES gnuradio-xzyblocks
    HINTS $ENV{XZYBLOCKS_DIR}/lib
        ${PC_XZYBLOCKS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(XZYBLOCKS DEFAULT_MSG XZYBLOCKS_LIBRARIES XZYBLOCKS_INCLUDE_DIRS)
MARK_AS_ADVANCED(XZYBLOCKS_LIBRARIES XZYBLOCKS_INCLUDE_DIRS)

