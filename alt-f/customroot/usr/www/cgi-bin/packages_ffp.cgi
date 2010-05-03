#!/bin/sh

. common.sh

check_cookie
write_header "ffp Package Manager"

s="<strong>"
es="</strong>"

if ! test -d /ffp/var/packages; then

	disks=$(ls /dev/sd?) >/dev/null 2>&1

	if test -z "$disks"; then
		echo "<br> $s No disks found! $es <br>"
		echo "</body></html>"
		exit 1
	fi

  cat<<EOF
	<h4>No ffp instalation found, install ffp in:</h4>
	<form action="/cgi-bin/packages_ffp_proc.cgi" method=post>
EOF
	select_part
	echo "</select><input type=submit name=install value=Install>
	</form></body></html>"

else

	echo "<h4 align=center>Warning: configuration files are
		overwritten when updating</h4>"
							
	inst_pkg=$(ls /ffp/var/packages)
	
	wget http://www.inreto.de/dns323/fun-plug/0.5/packages/ \
		-O /tmp/index.html >/dev/null 2>&1
	
	avail_pkg=$(awk -F \" '/href.*tgz/{print substr($4, 0, length($4)-4)}' \
		/tmp/index.html)
	
	wget http://www.inreto.de/dns323/fun-plug/0.5/extra-packages/All/ \
		-O /tmp/index.html >/dev/null 2>&1
	
	avail_pkg="$avail_pkg $(awk -F \" '/href.*tgz/{print substr($4, 0, length($4)-4)}' \
		/tmp/index.html)"
	
	rm /tmp/index.html
	
	cat <<-EOF
		<form action="/cgi-bin/packages_ffp_proc.cgi" method=post>
		<fieldset><legend> $s Installed Packages $es </legend><table>
	EOF
	
	for i in $inst_pkg; do
		#pkg_ver=$(echo $i | grep -o -e '-[-0-9.]*')
		base_name=${i%-*-*}
		echo "<tr><td><a href=\"http://www.inreto.de/dns323/fun-plug/0.5/PACKAGES.html#$base_name\">$i</a></td>"
		echo "<td><input type=submit name=$i value=Remove></td>"
					echo "$avail_pkg" | grep -q $i
					if test $? = "0"; then
						echo "<td><td>"
					else
						update_name=$(echo "$avail_pkg" | grep $base_name)
						if test -n "$update_name"; then
				to_update="$to_update $update_name"
							echo "<td><input type=submit name="$update_name" value=Update ></td>"
						fi
					fi
#		if test -f "/ffp/etc/www/${base_name}.html"; then
#			echo "<td><a href="/ffp/etc/www/${base_name}.html">Configure</a></td>" # FIXME
#		fi
		echo "</tr>"
	done
	
	cat <<-EOF
		</table></fieldset><br><fieldset><legend>
		<a href="http://www.inreto.de/dns323/fun-plug/0.5/">
		$s FFP Available Packages $es </a></legend><table>
	EOF
	
	for i in $avail_pkg; do
		if test -z "$(echo $inst_pkg | grep $i)"; then
			base_name=${i%-*-*}
			if test -z "$(echo $to_update | grep $base_name)"; then
				pkg_ver=$(echo $i | grep -o -e '-[-0-9.]*')
				echo "<tr><td><a href=\"http://www.inreto.de/dns323/fun-plug/0.5/PACKAGES.html#$base_name\">$i</a></td>"
				echo "<td><input type=submit name=$i value=Install></td><tr>"
			fi
		fi
	done
	
	echo "</table></fieldset></form></body></html>"
fi
