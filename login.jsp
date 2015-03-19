<HTML>
<HEAD>
<TITLE>Login</TITLE>
</HEAD>

<BODY>

<%@ page import="java.sql.*"%>
<%@ page import="java.util.*"%>

<% 

        if(request.getParameter("bSubmit") != null) {

	        //get the user input from the login page
        	String userName = (request.getParameter("USERID")).trim();
	        String passwd = (request.getParameter("PASSWD")).trim();
            //debug
        	//out.println("<p>Your input User Name is "+userName+"</p>");
        	//out.println("<p>Your input password is "+passwd+"</p>");


	        //establish the connection to the underlying database
        	Connection conn = null;
	
	        String driverName = "oracle.jdbc.driver.OracleDriver";
            String dbstring = "jdbc:oracle:thin:@gwynne.cs.ualberta.ca:1521:CRS";
            session.setAttribute("driverName", driverName);
            session.setAttribute("dbstring", dbstring);
	
	        try{
		        //load and register the driver
        		Class drvClass = Class.forName(driverName); 
	        	DriverManager.registerDriver((Driver) drvClass.newInstance());
        	} catch(Exception ex){
		        out.println("<hr>" + ex.getMessage() + "<hr>");
	
	        }
	
        	try{
	        	//establish the connection 
		        conn = DriverManager.getConnection(dbstring,"cdingram","Oracle_88");
        		conn.setAutoCommit(false);
	        } catch(Exception ex){
	        
		        out.println("<hr>" + ex.getMessage() + "<hr>");
        	}
	

	        //select the user table from the underlying db and validate the user name and password
        	Statement stmt1 = null;
	        ResultSet rset1 = null;
            Statement stmt2 = null;
            ResultSet rset2 = null;
        	String sqlPass = "SELECT password FROM users WHERE user_name = '"+userName+"'";
            String sqlClass = "SELECT class, person_id FROM users WHERE user_name = '"+userName+"'";
            //debug
	        //out.println(sql);
        	try{
	        	stmt1 = conn.createStatement();
		        rset1 = stmt1.executeQuery(sqlPass);

                stmt2 = conn.createStatement();
                rset2 = stmt2.executeQuery(sqlClass);

        	} catch(Exception ex){
		        out.println("<hr>" + ex.getMessage() + "<hr>");
        	}

	        String truepwd = "";
            String trueClass = "";
            int person_id = 0;
	
        	while(rset1 != null && rset1.next()) {
	        	truepwd = (rset1.getString(1)).trim();
	        }

            while(rset2 != null && rset2.next()) {
                trueClass = rset2.getString("class");
                person_id = rset2.getInt("person_id");

            }

        	//display the result
	        if(passwd.equals(truepwd)) {
                session.setAttribute("userName", userName);
                session.setAttribute("classType", trueClass);
                session.setAttribute("person_id", person_id);
                String homePage = "homePage.jsp";
		        response.sendRedirect(homePage);

        	} else {
                out.println("<H1><CENTER>Radiology Information System</CENTER></H1>");
	        	out.println("<p><b>Either your Username or Your Password is Invalid!</b></p>");
                out.println("<form method=post action=login.jsp>");
                out.println("UserName: <input type=text name=USERID maxlength=20><br>");
                out.println("Password: <input type=password name=PASSWD maxlength=20><br>");
                out.println("<input type=submit name=bSubmit value=Submit>");
                out.println("</form>");

                try{
                        conn.close();
                }
                catch(Exception ex){
                        out.println("<hr>" + ex.getMessage() + "<hr>");
                }
            }
        } else {
                out.println("<H1><CENTER>Radiology Information System</CENTER></H1>");
                out.println("<form method=post action=login.jsp>");
                out.println("UserName: <input type=text name=USERID maxlength=20><br>");
                out.println("Password: <input type=password name=PASSWD maxlength=20><br>");
                out.println("<input type=submit name=bSubmit value=Login>");
                out.println("</form>");
        }      
%>



</BODY>
</HTML>

