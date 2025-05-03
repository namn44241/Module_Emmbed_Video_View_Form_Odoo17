# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import os
import re

class TaiLieuHuongDan(models.Model):
    _name = 'tai_lieu_huong_dan'
    _description = 'Tài liệu hướng dẫn'
    
    name = fields.Char(string='Tên tài liệu', required=True)
    description = fields.Text(string='Mô tả')
    file_attachment = fields.Binary(string='Tệp đính kèm', required=True, attachment=True)
    file_name = fields.Char(string='Tên file')
    
    @api.constrains('file_name')
    def _check_file_extension(self):
        for record in self:
            if record.file_name:
                ext = os.path.splitext(record.file_name)[1].lower()
                if ext != '.pdf':
                    raise ValidationError(_('Tệp đính kèm phải là file PDF!'))

class VideoHuongDan(models.Model):
    _name = 'video_huong_dan'
    _description = 'Video hướng dẫn'
    
    name = fields.Char(string='Tên video', required=True)
    description = fields.Text(string='Mô tả')
    youtube_url = fields.Char(string='YouTube URL', required=True)
    youtube_embed = fields.Html(string='Embedded Video', compute='_compute_youtube_embed', sanitize=False)
    youtube_video_id = fields.Char(string='YouTube Video ID', compute='_compute_youtube_video_id')
    
    @api.depends('youtube_url')
    def _compute_youtube_video_id(self):
        for record in self:
            video_id = False
            if record.youtube_url:
                if 'youtube.com' in record.youtube_url and 'v=' in record.youtube_url:
                    video_id = record.youtube_url.split('v=')[1].split('&')[0]
                elif 'youtu.be' in record.youtube_url:
                    video_id = record.youtube_url.split('/')[-1].split('?')[0]
            record.youtube_video_id = video_id
    
    @api.depends('youtube_video_id')
    def _compute_youtube_embed(self):
        for record in self:
            if record.youtube_video_id:
                record.youtube_embed = f'<iframe width="100%" height="500" src="https://www.youtube.com/embed/{record.youtube_video_id}" frameborder="0" allowfullscreen="true"></iframe>'
            else:
                record.youtube_embed = '<p></p>' 
    
    @api.constrains('youtube_url')
    def _check_youtube_url(self):
        youtube_regex = r'^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+$'
        for record in self:
            if record.youtube_url and not re.match(youtube_regex, record.youtube_url):
                raise ValidationError(_('URL phải là link YouTube hợp lệ!'))