exam.php

<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    </head>
    <body>

<?php
session_start();
class exam
{
    public function __construct($user,$password,$host,$dbname)
    {
        //$this->data=$data;
        $this->user=$user;
        $this->password=$password;
        $this->host=$host;
        $this->dbname=$dbname;
        $this->dsn="mysql:host=$host;dbname=$dbname";
    }

    public function connect()
    {
        try{
            $db=new PDO($this->dsn,$this->user,$this->password);
            $db->exec("set names utf8");
            //echo "Connection successful.";
            return $db;
        }
        catch(PDOException $e)
        {
            echo "Connection error".$e;
            exit;
        }

    }

    public function select()
    {
        $db = $this->connect();
        //echo "hello!";
        $sql = "SELECT * FROM xjtk WHERE id=?";
        $num = rand(1, 2301);
        //print_r($num);
        $stmt = $db->prepare($sql);
        //print_r($stmt);
        $stmt->execute(array($num));
        $option=array("Question","A","B","C","D","E","Answer");
        $temp=array("question","option_a","option_b","option_c","option_d","option_e","question_answer");
        while ($row = $stmt->fetch(PDO::FETCH_ASSOC))
        {
            for($i=0;$i<6;$i++)
            {
                echo $option[$i];
                echo ":";
                echo $row[$temp[$i]];
                echo "</br>";
            }
            $_SESSION["row"]=$row;
            return $row;

        }
    }

    public function judge($answer)
    {
        $row=$_SESSION["row"];
        if($answer == $row["question_answer"])
        {
            return "Congratulate! You got it!";
        }
        else
        {
            //var_dump($_SESSION["row"]);
            //var_dump($row);
            echo "Your answer is wrong,the correct is ";
            echo $row["question_answer"];
            echo".";

        }
    }
}

?>
    </body>
</html>

