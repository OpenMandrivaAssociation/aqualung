%define		nonfree		0
%define		free		1

%global		_disable_rebuild_configure 1

%if 0%{nonfree}
# "Monkey's Audio Source Code License Agreement" is nonfree license.
%define		with_mac  --with-mac
%endif

%if 0%{free}
# The following packages are free license (patent issue).
%define		with_mpeg --with-mpeg
%define		with_lavc --with-lavc
%define		with_lame --with-lame
%endif

Summary:		Music Player for GNU/Linux
Name:		aqualung
Version:		2.0
Release:		1
License:		GPLv2+
Group:	Sound
Url:		https://aqualung.jeremyevans.net/
Source0:	https://github.com/jeremyevans/aqualung/archive/%{version}/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
# autogen.sh
BuildRequires:		autoconf
BuildRequires:		automake
BuildRequires:		pkgconfig
BuildRequires:		gettext-devel
# Desktop
BuildRequires:		desktop-file-utils
# GUI
BuildRequires:		pkgconfig(atk)
BuildRequires:		pkgconfig(cairo) 
BuildRequires:		pkgconfig(fontconfig)
BuildRequires:		pkgconfig(freetype2)
BuildRequires:		pkgconfig(glib-2.0) >= 2.72
BuildRequires:		pkgconfig(gtk+-3.0) >= 3.24
BuildRequires:		pkgconfig(libxml-2.0)
BuildRequires:		pkgconfig(libpng)
BuildRequires:		pkgconfig(pango)
BuildRequires:		pkgconfig(pixman-1)
BuildRequires:		pkgconfig(zlib)
# Output
BuildRequires:		pkgconfig(alsa)
BuildRequires:		pkgconfig(jack)
BuildRequires:		pkgconfig(libpulse)
BuildRequires:		pkgconfig(samplerate)
BuildRequires:		pkgconfig(sndio)
# Encode/Decode
%{?with_lavc:BuildRequires:	ffmpeg-devel}
%{?with_lame:BuildRequires:	lame-devel}
BuildRequires:		libmpcdec-devel
BuildRequires:		pkgconfig(flac)
BuildRequires:		pkgconfig(libmodplug) >= 0.8.4
BuildRequires:		pkgconfig(lrdf) >= 0.4.0
%{?with_mac:BuildRequires:	pkgconfig(mac)}
%{?with_mpeg:BuildRequires:	pkgconfig(mad)}
BuildRequires:		pkgconfig(oggz)
BuildRequires:		pkgconfig(sndfile) >= 1.0.18
BuildRequires:		pkgconfig(speex)
BuildRequires:		pkgconfig(vorbisfile)
BuildRequires:		pkgconfig(wavpack) >= 4.40.0
# CD
BuildRequires:		libcdio-paranoia-devel
BuildRequires:		pkgconfig(libcddb)
BuildRequires:		pkgconfig(libcdio)
# Others
BuildRequires:		libifp-devel
BuildRequires:		pkgconfig(libusb)
BuildRequires:		pkgconfig(luajit)
BuildRequires:		pkgconfig(raptor2)

%description
Aqualung is an advanced music player originally targeted at the GNU/Linux
operating system. It plays audio CDs, internet radio streams and pod casts as
well as sound files in just about any audio format and has the feature of
inserting no gaps between adjacent tracks.

%files -f %{name}.lang
%doc AUTHORS ChangeLog COPYING 
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/
%{_datadir}/doc/%{name}/*
%{_datadir}/%{name}/*
%{_datadir}/man/man1/%{name}.*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

#-----------------------------------------------------------------------------

%patchlist
aqualung-luajit.patch


%prep
%autosetup -p1
./autogen.sh


%build
%configure \
    --with-sndio \
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
