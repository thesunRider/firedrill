<?php

#create global shareable sessions
function generate_id() {
	$sessionid = 'A111A135818';
	return $sessionid;
}


$nchanels = 2;

session_id(generate_id());
session_start();

#create sessions variables
for ($x = 0; $x < $nchanels; $x++) {
	#ifpost was about channelvariable then set one
	if (isset($_POST['chnl'.$x]) && !empty($_POST['chnl'.$x])) {
		$_SESSION['chnl'.$x] =  $_POST['chnl'.$x];
	}
}

#query /?action=post
#query /?action=recv&channel=chnl1
#query /?action=check&channel=chnl1
#query /?action=terminate


if (isset($_GET["action"])) {
	#set session variables by posting
	if ($_GET["action"] == "post") {
		for ($i=0; $i < $nchanels; $i++) { 
			$add .= '<input name = "chnl'. $i .'" type="hidden" />	';	
		}
		echo '
		<html>
		<body>

		<form action = "<?php $_PHP_SELF ?>" method = "POST">'. $add .
		'
		<input type = "submit" />
		</form>

		</body>
		</html>';
	} 

	#recv data from channel
	elseif ($_GET["action"] == "recv") {
		if (isset($_GET["channel"])) {
			echo $_SESSION[$_GET["channel"]];
			#reset channel
		    $unset = $_GET["channel"];
			unset($_SESSION[$unset]);
		}
		else
		{
			echo "Specify channel";
		}
	}
	#check if a channel has data
	elseif ($_GET["action"] == "check") {
		if (isset($_GET["channel"])) {
			if (empty($_SESSION[$_GET["channel"]])) {
				#no data
				echo 0;
			}else
			{
				#has data
				echo 1;
			}
		}
	}
	#destroy all session variables
	elseif ($_GET["action"] == "terminate") {
		session_destroy();
		echo "Session destroyed";
	}
	else {
		echo "Specify a valid action";
	}
}
else {
	echo "Specify a valid parameter";
}

?>
