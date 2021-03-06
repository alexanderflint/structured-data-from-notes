SELECT 	
encdate, pat_mrn_id, pat_name, notedate,	
Max(case when line = 1 then note_text else '' end) ||
Max(case when line = 2 then note_text else '' end) ||
Max(case when line = 3 then note_text else '' end) ConcatenatedText
	
FROM 	
(SELECT DISTINCT c.contact_date encdate, d.pat_mrn_id, d.pat_name, a.create_instant_dttm notedate, b.line,b.note_text 	
FROM hno_info a INNER JOIN hno_note_text b ON a.note_id = b.note_id 	
INNER JOIN pat_enc_hsp c ON a.pat_enc_csn_id = c.pat_enc_csn_id 	
INNER JOIN patient d ON a.pat_id = d.pat_id 	
INNER JOIN 	
	(SELECT note_id, max(contact_date_real) MaxContactDate from hno_note_text 
	WHERE 
	note_text LIKE '%regstrkdatnte92tkL76s3%' 
	AND hno_note_text.contact_date between CAST('09/01/2015' as date format 'mm/dd/yyyy') and CAST('7/31/2016' as date format 'mm/dd/yyyy')
	GROUP BY note_id) x 
	ON a.note_id = x.note_id and b.contact_date_real = x.MaxContactDate
) y	
	
GROUP BY encdate, pat_mrn_id, pat_name, notedate	
ORDER BY encdate, pat_mrn_id, pat_name, notedate	

