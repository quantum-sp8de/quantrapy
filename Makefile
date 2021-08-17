DEB_PKGR='packaging/deb/build_deb.sh'

all:

deb:
	$(DEB_PKGR)
	cp deb_dist/python3-quantralib*deb ./


.PHONY: clean
clean:
	rm -rf deb_dist/ dist/ quantralib.egg-info/ build/ quantralib*tar.gz
