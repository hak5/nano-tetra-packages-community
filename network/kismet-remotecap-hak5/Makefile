include $(TOPDIR)/rules.mk

PKG_NAME:=kismet-remotecap-hak5
PKG_VERSION:=2021-05-R1
PKG_RELEASE:=1

PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)
PKG_SOURCE_PROTO:=git
PKG_SOURCE_URL:=https://github.com/kismetwireless/kismet.git
PKG_SOURCE_VERSION:=149efea60214f473c9ec9b16e50c3b22a8a874d0
PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION)-$(PKG_SOURCE_VERSION).tar.gz
PKG_SOURCE_SUBDIR:=$(PKG_NAME)-$(PKG_VERSION)

include $(INCLUDE_DIR)/package.mk

PKG_USE_MIPS16:=0

HOST_BUILD_DEPENDS:=protobuf/host

define Package/kismet-remotecap-hak5
  SECTION:=net
  CATEGORY:=Network
  TITLE:=Kismet Remote Capture (Hak5)
  URL:=https://www.kismetwireless.net/
  DEPENDS:=+libpthread +libpcap +libpcre +libmicrohttpd +libnl +libcap +libstdcpp +libncurses +libsqlite3 +zlib +protobuf-lite +libprotobuf-c +libdw +libwebsockets-full
  SUBMENU:=wireless
endef

define Package/kismet-remotecap-hak5/description
	Kismet Wireless Remote Capture Tools.
endef

define Build/Configure
  $(call Build/Configure/Default,--with-linux-headers=$(LINUX_DIR))
endef

CONFIGURE_ARGS += \
	--sysconfdir=/etc/kismet \
	--bindir=/usr/bin \
	--disable-python-tools \
	--with-protoc=$(STAGING_DIR_HOSTPKG)/bin/protoc \
	--enable-capture-tools-only

# Override libs to force lpthread because we don't detect it properly on openwrt
CONFIGURE_VARS += \
	CXXFLAGS="$$$$CXXFLAGS"  \
	LIBS="-lm -lpthread"

define Build/Compile
	$(MAKE) -C $(PKG_BUILD_DIR) \
		LD="$(TARGET_CXX)" \
		datasources
	gzip -d $(PKG_BUILD_DIR)/conf/kismet_manuf.txt.gz
endef

define Package/kismet-remotecap-hak5/install
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/kismet_cap_pcapfile $(1)/usr/bin/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/kismet_cap_kismetdb $(1)/usr/bin/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/capture_linux_wifi/kismet_cap_linux_wifi $(1)/usr/bin/
	$(INSTALL_BIN) $(PKG_BUILD_DIR)/capture_linux_bluetooth/kismet_cap_linux_bluetooth $(1)/usr/bin/

	$(INSTALL_DIR) $(1)/etc/kismet/
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/conf/kismet.conf $(1)/etc/kismet
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/conf/kismet_80211.conf $(1)/etc/kismet
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/conf/kismet_alerts.conf $(1)/etc/kismet
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/conf/kismet_filter.conf $(1)/etc/kismet
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/conf/kismet_httpd.conf $(1)/etc/kismet
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/conf/kismet_logging.conf $(1)/etc/kismet
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/conf/kismet_memory.conf $(1)/etc/kismet
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/conf/kismet_uav.conf $(1)/etc/kismet
	$(INSTALL_CONF) $(PKG_BUILD_DIR)/conf/kismet_manuf.txt $(1)/etc/kismet

	$(INSTALL_DIR) $(1)/usr/share/kismet/httpd/
	cp -Rv $(PKG_BUILD_DIR)/http_data/* $(1)/usr/share/kismet/httpd/
endef

$(eval $(call BuildPackage,kismet-remotecap-hak5))
