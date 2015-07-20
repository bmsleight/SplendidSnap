from django.core.management.base import BaseCommand, CommandError

from appsplendid.models import Splendid
import _libspendidsnap, random, shutil

class Command(BaseCommand):
#    args = '<poll_id poll_id ...>'
    help = 'Makes PDF where one does not exist'

    def handle(self, *args, **options):
        pack = Splendid.objects.filter(pdf="")[0]
        if pack:
            self.stdout.write('Pack 1: "%s"' % pack)
            texts = []
            images = []
            image_zip_name = ""
            if pack.words:
                texts = pack.words.split(",")
                texts = filter(None, texts)
                text_images = _libspendidsnap.list_of_images_from_text(texts)
                images = text_images
            if pack.image_zip_file:
                image_zip_name = pack.image_zip_file
                tmp_imagesdir = unpack_flat(pack.image_zip_file)
                images = images + glob.glob(tmp_imagesdir + '/*')
            self.stdout.write('Texts: "%s"' % texts)
            self.stdout.write('Images: "%s"' % images)

            arrangements, total_needed = _libspendidsnap.simple_card_list(pack.images_per_card-1)
            random.shuffle(images)
            real_pack = _libspendidsnap.Pack(images[:total_needed])
            for arrangement in arrangements:
                real_pack.make_card(arrangement)

            _libspendidsnap.generate__a4_pdf_from_images_list(images_filenames_list=real_pack.cards, 
                                                              pdf_name="/tmp/testing.pdf",
                                                              pack_name = pack.pack_name,
                                                              creator = pack.creator,
                                                              images_per_card =pack.images_per_card,
                                                              word_list = texts,
                                                              image_zip_name = image_zip_name,
                                                              source_of_images = pack.source_of_images,
                                                              
)
            _libspendidsnap.clean_up(real_pack.cards + real_pack.list_of_thumbs() + real_pack.images_filenames_list)
            _libspendidsnap.clean_up(text_images)
            if pack.image_zip_file:
                shutil.rmtree(tmp_imagesdir)


