include $(TOPDIR)/rules.mk

PKG_NAME:=backdoorfactory
PKG_VERSION:=0.2
PKG_RELEASE:=1

GO_PKG:=github.com/Binject/backdoorfactory

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://codeload.github.com/Binject/backdoorfactory/tar.gz/v${PKG_VERSION}?
PKG_HASH:=47bd0ea9bc390843e29e44873a298785a75ad08cc75d5c730b5007386b188c54
PKG_BUILD_DIR:=$(BUILD_DIR)/$(PKG_NAME)-$(PKG_VERSION)

PKG_LICENSE:=GPL-3.0
PKG_LICENSE_FILES:=LICENSE
PKG_MAINTAINER:=Benjamin Kurtz <awgh@awgh.org>

PKG_BUILD_DEPENDS:=golang/host
PKG_BUILD_PARALLEL:=1
PKG_USE_MIPS16:=0

include $(INCLUDE_DIR)/package.mk
include ../../lang/golang/golang-package.mk

define Package/backdoorfactory/Default
  TITLE:=A MitM tool for inserting shellcode into all types of binaries on the wire.
  URL:=https://binject.github.io/backdoorfactory
  DEPENDS:=$(GO_ARCH_DEPENDS) bettercap
endef

define Package/backdoorfactory
$(call Package/backdoorfactory/Default)
  SECTION:=net
  CATEGORY:=Network
endef

define Package/backdoorfactory/description
backdoorfactory is an extension to bettercap that allows the insertion of shellcode into intercepted file downloads.

It lets you man-in-the-middle web file downloads and inject them with platform-appropriate shellcode. It works on downloaded archives as well.

Features
* Works on PE, Mach-O, and ELF format binaries using the Binject Debug library
* Integrates with bettercap's DNS and ARP based man-in-the-middling capabilites
* Unpacks and repacks Zip, Tar, and Tar.gz archives, injecting any binaries inside
* Supports configurable methods of shellcode injection via the Binjection library
* Shellcode repository allows different shellcodes per architecture and per binary format
endef

define Package/backdoorfactory/install
	$(call GoPackage/Package/Install/Bin,$(PKG_INSTALL_DIR))
	$(INSTALL_DIR) $(1)/usr/bin
	$(INSTALL_BIN) $(PKG_INSTALL_DIR)/usr/bin/backdoorfactory  $(1)/usr/bin/backdoorfactory
endef

$(eval $(call GoBinPackage,backdoorfactory))
$(eval $(call BuildPackage,backdoorfactory))


