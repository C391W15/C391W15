<HTML>
<HEAD>
<TITLE>Change Password</TITLE>
</HEAD>

<BODY>

<%@ page import="java.sql.*"%>
<%@ page import="java.util.*"%>

<%

	
	if(request.getParameter("new1") != null && request.getParameter("new2") != null) {

	    String new1 = (request.getParameter("new1")).trim();
	    String new2 = (request.getParameter("new2")).trim();

	    if(new1 != "" && new2 != "") {
	    	if(new1.equals(new2)) {

	    		Connection conn = null;
	    		String driverName = (String) session.getAttribute("driverName");
	    		String dbstring = (String) session.getAttribute("dbstring");



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

	        	String userName = (String) session.getAttribute("userName");
	        	String sql = "UPDATE users SET password = '" + new1 + "' WHERE user_name = '"+userName+"'";
	        	Statement stmt = null;

	        	try{
		        	stmt = conn.createStatement();
		        	stmt.executeUpdate(sql);
		        	conn.close();
		        	out.println("<H1><CENTER>Change Password</CENTER></H1>");
		       		out.println("<p>Password Changed</p>");
					out.println("<form method=post action=homePage.jsp>");
				    out.println("<input type=submit name=backPWD value=Back>");
				    out.println("</form>");
				    out.println("<form method=post action=changePWD.jsp>");
				    out.println("New Password: <input type=password name=new1 maxlength=20><br>");
				    out.println("Re-Enter New Password: <input type=password name=new2 maxlength=20><br>");
				    out.println("<input type=submit name=bSubmit value=Change>");
				    out.println("</form>");

	        	} catch(Exception ex){
			        out.println("<hr>" + ex.getMessage() + "<hr>");
	        	}

	        	

	    	} else {
	    		out.println("<H1><CENTER>Change Password</CENTER></H1>");
	    		out.println("<p>Passwords Don't Match, Please Try Again</p>");
				out.println("<form method=post action=homePage.jsp>");
			    out.println("<input type=submit name=backPWD value=Back>");
			    out.println("</form>");
			    out.println("<form method=post action=changePWD.jsp>");
			    out.println("New Password: <input type=password name=new1 maxlength=20><br>");
			    out.println("Re-Enter New Password: <input type=password name=new2 maxlength=20><br>");
			    out.println("<input type=submit name=bSubmit value=Change>");
			    out.println("</form>");
	    	}
		} else {
			out.println("<H1><CENTER>Change Password</CENTER></H1>");
			out.println("<p>Invalid, Please Try Again</p>");
			out.println("<form method=post action=homePage.jsp>");
		    out.println("<input type=submit name=backPWD value=Back>");
		    out.println("</form>");
		    out.println("<form method=post action=changePWD.jsp>");
		    out.println("New Password: <input type=password name=new1 maxlength=20><br>");
		    out.println("Re-Enter New Password: <input type=password name=new2 maxlength=20><br>");
		    out.println("<input type=submit name=bSubmit value=Change>");
		    out.println("</form>");
		}
	} else {

		out.println("<H1><CENTER>Change Password</CENTER></H1>");
		out.println("<form method=post action=homePage.jsp>");
	    out.println("<input type=submit name=backPWD value=Back>");
	    out.println("</form>");
	    out.println("<form method=post action=changePWD.jsp>");
	    out.println("New Password: <input type=password name=new1 maxlength=20><br>");
	    out.println("Re-Enter New Password: <input type=password name=new2 maxlength=20><br>");
	    out.println("<input type=submit name=bSubmit value=Change>");
	    out.println("</form>");
	}
%>

</Body>
</HTML>
