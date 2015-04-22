Add creation and modification timestamps to an Excel worksheet
##############################################################


:date: 2002-02-19 09:00
:tags: data quality, excel, vba
:category: programming


Please, for the love of $deity do not hit me….. This is going to be a post
about excel!

Excel is a horrid solution for data entry, and even worse for data archival.
And yet, it’s one of the most commonly used solutions. One of the most useful
information in any given data-set is the information about when the information
was created and when it was last modified. This is something that any decent
developer in charge of a data collection (let’s just call it that for now) will
add to each data record.

Alas, a lot of non-IT people manage and store their data in excel worksheets.
And that is OK with me as long as they pay attention to data archival. In it’s
most simple form, data archival can be achieved by storing the data as a CSV
file and including the following metadata:

* Which column represents which value (the name of the variable)
* The data type (f.ex.: number, text, date, …) of each column
* If a column is “coded”, please also include the meaning of each code.
  For example a “Yes”, “No”, “Maybe” column might be stored as “1”, “2” and
  “3”. Which means in it’s most basic nature it’s a numeric variable, but the
  different values have a meaning attached to them. So: Add this list in your
  metadata description.
* If any computations or checks are performed on the values, please add them to
  the metadata document as well!

Even if the timestamp values might seem superflous at first, it will be of
great help to anyone tracing errors in the data. Imagine that you would at some
point need to fix some values that were entered/modified during a specific time
period for whatever reason. Without this most basic bit of information you will
be up for a treat. However, if it’s been rigurously implemented since the
beginning, you’ll have the problem solved in no time.

Now, each halfway serious database system will offer you this kind of
functionality out-of-the-box. But Excel is no database system (I intentionally
left out the word “management” as this issue is a bit more general!). So it
does not offer you a straight-forward way to solve this. But even if it’s not
straight-forward, it’s simple enough for about anyone using Excel do add this
bit of information.

Assuming that you use the first two columns (numbered 1 and 2 in excel) of your
worksheet to add creation- and modification timestamps simply open up the
Visual Basic editor (found in Tools->Macro or somesuch), next, in your project
tree (in the top left of the screen) select your workbook (the .xls file), and
in it’s sub-tree double-click the Worksheet that should have the timestamps set
automatically.

Then copy/paste the following text into the just opened code editor and you’re
done. I hope the comments will give some insight as to what happens. Note that
in this case I will ignore the first row of the sheet, and obviously, the first
two columns. If that does not suit your needs, feel free to change this script
to your liking.


.. code-block:: vb.net

    '
    ' Callback which is called when a cell in a workbook changes
    ' @param Target: The cell that changed it's value
    '
    Private Sub Worksheet_Change(ByVal Target As Range)
      ' We will ignore any changes in the first row, as it contains header
      ' labels
      If Target.Row = 1 Then Exit Sub
      ''

      ' As we set the values of column 1 and 2 we won't need to capture
      ' changes in these either
      If Target.Column = 1 Or Target.Column = 2 Then Exit Sub
      ''

      ' We will update the timestamp in column 2 *always* (last changed time)
      Cells(Target.Row, 2) = Now

      ' We will update the timestamp in column 1 only if it is empty (creation
      ' time)
      If IsEmpty(Cells(Target.Row, 1)) Then
         Cells(Target.Row, 1) = Now
       End If
    End Sub
