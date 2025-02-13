%global         nonfree  0
%global         free     1

%define _disable_rebuild_configure 1

%if 0%{nonfree}
# "Monkey's Audio Source Code License Agreement" is nonfree license.
%global         with_mac  --with-mac
%global		with_lame --with-lame
%endif

%if 0%{free}
# The following packages are free license (patent issue).
%global         with_mpeg --with-mpeg
%global         with_lavc --with-lavc
%endif

Name:           aqualung
Version:        1.2
Release:        1
Summary:        Music Player for GNU/Linux
Group:          Sound
License:        GPLv2+
URL:            https://aqualung.jeremyevans.net/
Source0:        https://github.com/jeremyevans/aqualung/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}.desktop
# autogen.sh
BuildRequires:  autoconf automake pkgconfig gettext-devel
# GUI
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0) pkgconfig(atk) cairo-devel pango-devel
BuildRequires:  pkgconfig(pixman-1) pkgconfig(libpng) pkgconfig(zlib)
BuildRequires:  pkgconfig(fontconfig) pkgconfig(freetype2) pkgconfig(libxml-2.0)
# Desktop
BuildRequires:  desktop-file-utils
# Output
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(samplerate)
# Encode/Decode
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(vorbisfile)
BuildRequires:  pkgconfig(oggz)
BuildRequires:  pkgconfig(speex)
%{?with_mpeg:BuildRequires:  pkgconfig(mad)}
BuildRequires:  pkgconfig(libmodplug)
BuildRequires:  libmpcdec-devel
%{?with_mac:BuildRequires:  pkgconfig(mac)}
%{?with_lavc:BuildRequires:  ffmpeg-devel}
%{?with_lame:BuildRequires:  lame-devel}
BuildRequires:  pkgconfig(wavpack)
BuildRequires:  pkgconfig(lrdf)
# CD
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  libcdio-paranoia-devel
BuildRequires:  pkgconfig(libcddb)
# Others
BuildRequires:  pkgconfig(libusb)
BuildRequires:  libifp-devel
BuildRequires:  pkgconfig(luajit)
BuildRequires:  pkgconfig(raptor2)

%description
Aqualung is an advanced music player originally targeted at the GNU/Linux
operating system. It plays audio CDs, internet radio streams and pod casts as
well as sound files in just about any audio format and has the feature of
inserting no gaps between adjacent tracks.

%prep
%autosetup -p1
./autogen.sh

%build
%configure \
    --without-sndio \
    --with-oss \
    --with-alsa \
    --with-jack \
    --with-pulse \
    --with-src \
    --with-sndfile \
    --with-flac \
    --with-vorbisenc \
    --with-speex \
    %{!?with_mpeg: --without-mpeg} %{?with_mpeg} \
    --with-mod \
    --with-mpc \
    %{!?with_mac:  --without-mac} %{?with_mac} \
    %{!?with_lavc: --without-lavc} %{?with_lavc} \
    %{!?with_lame: --without-lame} %{?with_lame} \
    --with-wavpack \
    --with-ladspa \
    --with-cdda \
    --with-cddb \
    --with-ifp \
    --with-lua


# Fix lib64 path
sed -i 's@/usr/lib/@%{_libdir}/@g' src/plugin.c

%make_build

%install
make install DESTDIR=%{buildroot} INSTALL="%{__install} -p -c"

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

install -d -m 755 %{buildroot}%{_datadir}/pixmaps
install -D -m 644 -p src/img/icon_48.png \
    %{buildroot}%{_datadir}/pixmaps/%{name}.png

%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING 
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/
%{_datadir}/doc/aqualung/*
%{_datadir}/%{name}/*
%{_datadir}/man/man1/%{name}.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
