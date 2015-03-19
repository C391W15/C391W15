<HTML>
<HEAD>
<TITLE>HomePage</TITLE>
</HEAD>

<BODY>

<%@ page import="java.sql.*"%>
<%@ page import="java.util.*"%>

<%
	String userName = (String) session.getAttribute("userName");
	String classType = (String) session.getAttribute("classType");

	out.println("<p><b>Your Login is Successful!</b></p>");
    out.println("<p>Welcome "+userName+"</p>");

    // allow password and info changes
    out.println("<form method=post action=changePWD.jsp>");
    out.println("<input type=submit name=changePWD value=ChangePassword>");
    out.println("</form>");
    out.println("<form method=post action=changeInfo.jsp>");
    out.println("<input type=submit name=changeInfo value=ChangePersonalInfo>");
    out.println("</form>");

    
    // display options based on user class
    if(classType.equals("a")) {
    	out.println("<p>Admin</p>");
        //out.println("<form method=post action=userManagment.jsp>");
        //out.println("<input type=submit name=managmentMod value=User Managment Module>");
        //out.println("</form>");
    } else {
        out.println("<p>"+classType+"</p>");
    }             
    

%>

</Body>
</HTML>
